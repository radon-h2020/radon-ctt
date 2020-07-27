import uuid
import os
import requests
import yaml

from flask import current_app
from sqlalchemy import Column, String, ForeignKey
from shutil import copytree, ignore_patterns, rmtree
from straight.plugin.loaders import ModuleLoader

from util.configuration import BasePath
from util.tosca_helper import Csar
from db_orm.database import Base, db_session
from models.project import Project
from models.abstract_model import AbstractModel


class TestArtifact(Base, AbstractModel):
    __tablename__ = 'testartifact'

    uuid: str
    commit_hash: str
    sut_tosca_path: str
    ti_tosca_path: str
    storage_path: str
    policy: str
    plugin: str
    project_uuid: str

    uuid = Column(String, primary_key=True)
    commit_hash = Column(String, nullable=False)
    sut_tosca_path = Column(String, nullable=False)
    ti_tosca_path = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    policy = Column(String, nullable=False)
    plugin = Column(String, nullable=False)
    project_uuid = Column(String, ForeignKey('project.uuid'), nullable=False)

    parentType = Project

    plugin_list = None

    def __init__(self, project, sut_tosca_path, ti_tosca_path, policy, plugin):
        self.uuid = str(uuid.uuid4())
        self.project_uuid = project.uuid
        self.sut_tosca_path = sut_tosca_path
        self.ti_tosca_path = ti_tosca_path
        self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)
        self.policy = policy
        self.plugin = plugin

        if not os.path.exists(self.fq_storage_path):
            os.makedirs(self.fq_storage_path)

        self.commit_hash = project.commit_hash

        # Copy repository excluding the '.git' directory
        src_dir = project.fq_storage_path
        if os.path.isdir(src_dir) and os.path.isdir(self.fq_storage_path):
            copytree(src_dir, self.fq_storage_path, ignore=ignore_patterns('.git'), dirs_exist_ok=True)

        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<TestArtifact UUID=%r, COMMIT_HASH=%r, SUT_PATH=%r, TI_PATH=%r, ST_PATH=%r, PR_UUID=%r >' % \
               (self.uuid, self.commit_hash, self.sut_tosca_path,
                self.ti_tosca_path, self.storage_path, self.project_uuid)

    def copy_test_config(self):
        test_plan = os.path.join(self.fq_storage_path, 'radon-ctt', 'test_plan.jmx')
        if os.path.isfile(test_plan):
            import shutil
            shutil.copy2(test_plan, '/tmp/test_plan.jmx')

    @property
    def fq_storage_path(self):
        return os.path.join(BasePath, self.storage_path)

    @property
    def policy_yaml(self):
        return yaml.full_load(self.policy)

    @property
    def handler_plugin(self):
        return self.plugin

    @classmethod
    def get_parent_type(cls):
        return Project

    @classmethod
    def create(cls, project_uuid, sut_tosca_location, ti_tosca_location):
        linked_project = Project.get_by_uuid(project_uuid)

        # Read property
        csar_as_url_env = os.getenv('CSAR_URL')

        # If present and set to "1"
        if csar_as_url_env and csar_as_url_env == "1":
            csar_as_url = True
            current_app.logger.info('CSAR as URL mode enabled.')
        else:
            csar_as_url = False
            current_app.logger.info('CSAR as URL mode disabled.')

        if csar_as_url:
            # Define default paths
            artifact_dir = os.path.join(linked_project.fq_storage_path, 'radon-ctt')
            sut_file_path = os.path.join(artifact_dir, 'sut.csar')
            ti_file_path = os.path.join(artifact_dir, 'ti.csar')

            # Create directory if it does not exist
            os.makedirs(artifact_dir, exist_ok=True)

            if TestArtifact.url_exists(sut_tosca_location):
                sut_file = requests.get(sut_tosca_location, allow_redirects=True)
                with open(sut_file_path, 'wb') as sut_csar_dl:
                    sut_csar_dl.write(sut_file.content)
                current_app.logger.info(f'Obtained SUT CSAR from "${sut_tosca_location}"')

            if TestArtifact.url_exists(ti_tosca_location):
                ti_file = requests.get(ti_tosca_location, allow_redirects=True)
                with open(ti_file_path, 'wb') as ti_csar_dl:
                    ti_csar_dl.write(ti_file.content)
                current_app.logger.info(f'Obtained TI CSAR from "${ti_tosca_location}"')
        else:
            sut_file_path = os.path.join(linked_project.fq_storage_path, sut_tosca_location)
            ti_file_path = os.path.join(linked_project.fq_storage_path, ti_tosca_location)

        test_artifact_list = []
        sut_policy_list = TestArtifact.parse_policies(sut_file_path)
        ti_blueprint = TestArtifact.parse_ti_metadata(ti_file_path)
        plugin_list = ModuleLoader().load('plugins')

        # Collect all available plugins
        plugins_available = []
        for plugin in plugin_list:
            plugins_available.append(plugin.plugin_type)
            current_app.logger.info(f'Plugin \'{plugin.plugin_type}\' found.')

        # Check which policies match the available plugins and which TI blueprint is present
        for policy in sut_policy_list:
            current_policy = sut_policy_list[policy]
            if current_policy['type'] in plugins_available:
                if current_policy['properties']['ti_blueprint'] == ti_blueprint:

                    sut_file_path_relative = os.path.relpath(sut_file_path, start=linked_project.fq_storage_path)
                    ti_file_path_relative = os.path.relpath(ti_file_path, start=linked_project.fq_storage_path)

                    # Policy matches existing TI blueprint, so test artifact will be created.
                    test_artifact_list.append(TestArtifact(linked_project, sut_file_path_relative, ti_file_path_relative,
                                                           yaml.dump(current_policy), current_policy['type']))
                    current_app.logger.info(f'Created test artifact for {ti_blueprint}.')
                else:
                    # No matching TI blueprint, so nothing to be done with this policy.
                    current_app.logger.info(f"The policy-defined TI blueprint "
                                            f"({current_policy['properties']['ti_blueprint']}) "
                                            f"does not match the TI model ({ti_blueprint}).")
            else:
                current_app.logger.info(f"Could not find matching plugin for {sut_policy_list[policy]['type']}.")

        return test_artifact_list

    @classmethod
    def parse_policies(cls, sut_file_path=None):
        if sut_file_path:
            with Csar(sut_file_path) as sut_csar:
                entry_point = sut_csar.tosca_entry_point
                sut_tosca = sut_csar.file_as_dict(entry_point)
                try:
                    return sut_tosca['topology_template']['policies']
                except LookupError as e:
                    current_app.logger.debug(f'Policies could not be found in {sut_file_path}.')

        else:
            return [
                {
                    'SimplePingTest': {
                        'type': 'radon.policies.testing.PingTest',
                        'properties': {
                            'hostname': 'localhost',
                            'ti_blueprint': 'radon.blueprints.DeploymentTestAgent',
                            'test_id': 'pingtest_123',
                        },
                        'targets': ['SockShop'],
                    }
                },
                {
                    'SimpleEndpointTest': {
                        'type': 'radon.policies.testing.HttpEndpointTest',
                        'properties': {
                            'path': "/cart/",
                            'hostname': 'localhost',
                            'method': "GET",
                            'port': 80,
                            'expected_status': 200,
                            'expected_body': None,
                            'ti_blueprint': None,
                            'use_https': False,
                            'test_body': None,
                            'test_header': None,
                            'test_id': None,
                        },
                        'targets': ['SockShop'],
                    }
                },
                {
                    'SimpleJMeterLoadTest': {
                        'type': 'radon.policies.testing.JMeterLoadTest',
                        'properties': {
                            'jmx_file': 'sockshop.jmx',
                            'hostname': 'localhost',
                            'port': 8080,
                            'ti_blueprint': 'radon.blueprints.testing.JMeterMasterOnly',
                            'user.properties': None,
                            'test_id': 'loadtest213',
                        },
                        'targets': ['SockShop'],
                    }
                }
            ]

    @classmethod
    def parse_ti_metadata(cls, ti_file_path):
        if ti_file_path:
            with Csar(ti_file_path) as ti_csar:
                entry_point = ti_csar.tosca_entry_point
                return ti_csar.file_ns_name(entry_point)

    @classmethod
    def get_all(cls):
        return TestArtifact.query.all()

    @classmethod
    def get_by_uuid(cls, get_uuid):
        return TestArtifact.query.filter_by(uuid=get_uuid).first()

    @classmethod
    def delete_by_uuid(cls, del_uuid):
        testartifact = TestArtifact.query.filter_by(uuid=del_uuid)
        if testartifact:
            folder_to_delete = testartifact.first().fq_storage_path
            from models.deployment import Deployment
            linked_deployments = Deployment.query.filter_by(testartifact_uuid=del_uuid)
            for result in linked_deployments:
                Deployment.delete_by_uuid(result.uuid)
            testartifact.delete()
            rmtree(folder_to_delete)
            db_session.commit()

    @classmethod
    def url_exists(cls, path):
        r = requests.head(path)
        return r.status_code == requests.codes.ok
