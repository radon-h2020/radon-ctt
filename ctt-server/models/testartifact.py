import tempfile
import uuid
import os
import requests
import yaml

from flask import current_app
from sqlalchemy import Column, String, ForeignKey
from shutil import copy, copytree, ignore_patterns, rmtree
from straight.plugin.loaders import ModuleLoader

from util.configuration import get_path, RepoDir
from util.tosca_helper import Csar
from db_orm.database import Base, db_session
from models.project import Project
from models.abstract_model import AbstractModel


class TestArtifact(Base, AbstractModel):
    __tablename__ = 'testartifact'

    uuid: str
    commit_hash: str
    sut_tosca_path: str
    sut_inputs_path: str
    ti_tosca_path: str
    ti_inputs_path: str
    storage_path: str
    policy: str
    plugin: str
    project_uuid: str

    uuid = Column(String, primary_key=True)
    commit_hash = Column(String, nullable=False)
    sut_tosca_path = Column(String, nullable=False)
    sut_inputs_path = Column(String, nullable=True)
    ti_tosca_path = Column(String, nullable=False)
    ti_inputs_path = Column(String, nullable=True)
    storage_path = Column(String, nullable=False)

    policy = Column(String, nullable=False)
    plugin = Column(String, nullable=False)
    project_uuid = Column(String, ForeignKey('project.uuid'), nullable=False)

    parentType = Project
    plugin_list = None

    sut_default_file_name = 'sut.csar'
    sut_inputs_default_file_name = 'sut-inputs.yaml'
    ti_default_file_name = 'ti.csar'
    ti_inputs_default_file_name = 'ti-inputs.yaml'

    def __init__(self, project, sut_tosca_path, sut_inputs_path, ti_tosca_path, ti_inputs_path, tmp_dir, policy, plugin):
        self.uuid = str(uuid.uuid4())
        self.project_uuid = project.uuid
        self.storage_path = os.path.join(get_path(), self.__tablename__, self.uuid)
        self.policy = policy
        self.plugin = plugin

        if not os.path.exists(self.fq_storage_path):
            os.makedirs(self.fq_storage_path)

        self.commit_hash = project.commit_hash

        # Copy repository excluding the '.git' directory
        src_dir = project.fq_storage_path
        if os.path.isdir(src_dir) and os.path.isdir(self.fq_storage_path):
            copytree(src_dir, self.fq_storage_path, ignore=ignore_patterns('.git'), dirs_exist_ok=True)

        # Set default paths for the artifacts and copy them into the testartifact folder in the RepoDir of RadonCTT
        self.sut_tosca_path = os.path.join(RepoDir, TestArtifact.sut_default_file_name)
        sut_tosca_path_fq = os.path.join(self.fq_storage_path, self.sut_tosca_path)
        os.makedirs(os.path.dirname(sut_tosca_path_fq), exist_ok=True)
        copy(sut_tosca_path, sut_tosca_path_fq)

        self.ti_tosca_path = os.path.join(RepoDir, TestArtifact.ti_default_file_name)
        ti_tosca_path_fq = os.path.join(self.fq_storage_path, self.ti_tosca_path)
        os.makedirs(os.path.dirname(ti_tosca_path_fq), exist_ok=True)
        copy(ti_tosca_path, ti_tosca_path_fq)

        if sut_inputs_path:
            self.sut_inputs_path = os.path.join(RepoDir, TestArtifact.sut_inputs_default_file_name)
            sut_inputs_path_fq = os.path.join(self.fq_storage_path, self.sut_inputs_path)
            os.makedirs(os.path.dirname(sut_inputs_path_fq), exist_ok=True)
            copy(sut_inputs_path, sut_inputs_path_fq)

        if ti_inputs_path:
            self.ti_inputs_path = os.path.join(RepoDir, TestArtifact.ti_inputs_default_file_name)
            ti_inputs_path_fq = os.path.join(self.fq_storage_path, self.ti_inputs_path)
            os.makedirs(os.path.dirname(ti_inputs_path_fq), exist_ok=True)
            copy(ti_inputs_path, ti_inputs_path_fq)

        db_session.add(self)
        db_session.commit()

        rmtree(tmp_dir, ignore_errors=True)

    def __repr__(self):
        return '<TestArtifact UUID=%r, COMMIT_HASH=%r, SUT_PATH=%r, TI_PATH=%r, ST_PATH=%r, PR_UUID=%r >' % \
               (self.uuid, self.commit_hash, self.sut_tosca_path,
                self.ti_tosca_path, self.storage_path, self.project_uuid)

    @property
    def fq_storage_path(self):
        return os.path.join(get_path(), self.storage_path)

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
    def create(cls, project_uuid, sut_tosca_location, sut_inputs_location, ti_tosca_location, ti_inputs_location):
        linked_project = Project.get_by_uuid(project_uuid)

        # Create temporary directory to collect all the artifacts (SUT, TI, inputs), as they might come from URL or path
        artifact_dir = tempfile.mkdtemp(prefix="radon-ctt")

        sut_file_path = os.path.join(artifact_dir, TestArtifact.sut_default_file_name)
        TestArtifact.process_resource(sut_tosca_location, sut_file_path, linked_project.fq_storage_path)

        ti_file_path = os.path.join(artifact_dir, TestArtifact.ti_default_file_name)
        TestArtifact.process_resource(ti_tosca_location, ti_file_path, linked_project.fq_storage_path)

        if sut_inputs_location:
            sut_inputs_path = os.path.join(artifact_dir, TestArtifact.sut_inputs_default_file_name)
            TestArtifact.process_resource(sut_inputs_location, sut_inputs_path, linked_project.fq_storage_path)
        else:
            sut_inputs_path = None

        if ti_inputs_location:
            ti_inputs_path = os.path.join(artifact_dir, TestArtifact.ti_inputs_default_file_name)
            TestArtifact.process_resource(ti_inputs_location, ti_inputs_path, linked_project.fq_storage_path)
        else:
            ti_inputs_path = None

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
        for policy_map in sut_policy_list:
            for policy in policy_map:
                current_policy = policy_map[policy]
                if current_policy['type'] in plugins_available:
                    if current_policy['properties']['ti_blueprint'] == ti_blueprint:

                        #sut_file_path_relative = os.path.relpath(sut_file_path, start=linked_project.fq_storage_path)
                        #ti_file_path_relative = os.path.relpath(ti_file_path, start=linked_project.fq_storage_path)

                        # Policy matches existing TI blueprint, so test artifact will be created.
                        test_artifact_list.append(TestArtifact(linked_project, sut_file_path, sut_inputs_path, ti_file_path,
                                                               ti_inputs_path, artifact_dir, yaml.dump(current_policy),
                                                               current_policy['type']))
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
    def __url_exists(cls, path):
        r = requests.head(path)
        return r.status_code == requests.codes.ok

    @classmethod
    def __is_url(cls, url_string):
        from rfc3987 import parse
        try:
            parse(url_string, rule='IRI')
            return True
        except ValueError:
            return False

    @classmethod
    def process_resource(cls, resource_string, resource_destination, storage_path):
        # Check if the resource is an URL
        if TestArtifact.__is_url(resource_string):
            current_app.logger.info(f'Resource {resource_string} is a valid URL.')
            if TestArtifact.__url_exists(resource_string):
                current_app.logger.info(f'URL {resource_string} exists.')
                resource_file = requests.get(resource_string, allow_redirects=True)
                with open(resource_destination, 'wb') as res_dest:
                    res_dest.write(resource_file.content)
                current_app.logger.info(f'Obtained resource from "${resource_string}"')
            else:
                current_app.logger.error(f'Resource {resource_string} is *NOT* a valid URL.')
                raise LookupError(f'Resource {resource_string} is *NOT* a valid URL.')
        # Check if it is a file
        elif os.path.isfile(os.path.join(storage_path, resource_string)):
            current_app.logger.info(f'Resource {resource_string} is a valid file.')
            copy(os.path.join(storage_path, resource_string), resource_destination)
        else:
            current_app.logger.error(f'Resource {resource_string} seems to be neither an URL nor a file.')
            raise LookupError(f'Resource {resource_string} seems to be neither an URL nor a file.')
