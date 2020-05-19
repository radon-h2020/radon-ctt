import glob
import os
import subprocess
import uuid
import yaml
import zipfile

from flask import current_app
from sqlalchemy import Column, String, ForeignKey

from db_orm.database import Base, db_session
from models.testartifact import TestArtifact
from models.abstract_model import AbstractModel
from util.configuration import BasePath, DropPolicies


class Deployment(Base, AbstractModel):
    __tablename__ = 'deployment'

    uuid: str
    testartifact_uuid: str
    storage_path: str
    status: str

    uuid = Column(String, primary_key=True)
    testartifact_uuid = Column(String, ForeignKey('testartifact.uuid'), nullable=False)

    def __init__(self, testartifact):
        self.uuid = str(uuid.uuid4())
        self.testartifact_uuid = testartifact.uuid
        self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)

        if testartifact:
            db_session.add(self)
            db_session.commit()
        else:
            raise Exception(f'Linked entities do not exist.')

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def __repr__(self):
        return '<Deployment UUID=%r, TA_UUID=%r>' % (self.uuid, self.testartifact_uuid)

    def deploy(self):
        test_artifact = TestArtifact.get_by_uuid(self.testartifact_uuid)
        sut_csar_path = os.path.join(test_artifact.fq_storage_path, test_artifact.sut_tosca_path)
        ti_csar_path = os.path.join(test_artifact.fq_storage_path, test_artifact.ti_tosca_path)

        tosca_meta_file_path = 'TOSCA-Metadata/TOSCA.meta'

        # Deployment of SuT
        if os.path.isfile(sut_csar_path):
            os.makedirs(self.sut_storage_path)

            # As soon as opera supports automatic extraction,
            # we do not need the extraction step anymore
            zipfile.ZipFile(sut_csar_path).extractall(self.sut_storage_path)
            entry_definition = Deployment.get_csar_entry_definition(
                os.path.join(self.sut_storage_path, tosca_meta_file_path))
            Deployment.drop_policies(self.sut_storage_path)
            #

            current_app.logger.\
                info(f'Deploying SuT {str(entry_definition)} with opera in folder {str(self.sut_storage_path)}.')
            subprocess.call(['opera', 'deploy', entry_definition], cwd=self.sut_storage_path)

        # Deployment of TI
        if os.path.isfile(ti_csar_path):
            os.makedirs(self.ti_storage_path)

            # As soon as opera supports automatic extraction,
            # we do not need the extraction step anymore
            zipfile.ZipFile(ti_csar_path).extractall(self.ti_storage_path)
            entry_definition = Deployment.get_csar_entry_definition(
                os.path.join(self.ti_storage_path, tosca_meta_file_path))
            Deployment.drop_policies(self.ti_storage_path)
            #

            if entry_definition:
                current_app.logger.\
                    info(f'Deploying TI {str(entry_definition)} with opera in folder {str(self.ti_storage_path)}.')
                subprocess.call(['opera', 'deploy', entry_definition], cwd=self.ti_storage_path)

    def undeploy(self):
        pass

    @property
    def base_storage_path(self):
        return self.storage_path

    @property
    def sut_storage_path(self):
        return os.path.join(self.storage_path, 'system_under_test')

    @property
    def ti_storage_path(self):
        return os.path.join(self.storage_path, 'test_infrastructure')

    @classmethod
    def get_csar_entry_definition(cls, tosca_meta_file='TOSCA-Metadata/TOSCA.meta'):
        if os.path.isfile(tosca_meta_file):
            with open(tosca_meta_file) as tosca_meta:
                for line in tosca_meta:
                    if line.startswith('Entry-Definitions: '):
                        return line.strip().split(' ')[1]
        raise Exception('Entry definition could not be found.')

    @classmethod
    def drop_policies(cls, folder):
        """Removes any occurrences of policy_type and policies-elements in the *.tosca files in the given folder."""

        # Drop policies enabled in the configuration?
        if DropPolicies:
            definitions_folder = os.path.join(folder, "_definitions")
            if os.path.isdir(folder) and os.path.isdir(definitions_folder):
                file_list = glob.glob(definitions_folder + os.sep + "*.tosca")
                if len(file_list) > 0:
                    for file in file_list:
                        with open(file, 'r') as tosca_file_in:
                            tosca_yaml = yaml.full_load(tosca_file_in)

                        if 'policy_types' in tosca_yaml:
                            del tosca_yaml['policy_types']
                        if 'topology_template' in tosca_yaml and 'policies' in tosca_yaml['topology_template']:
                            del tosca_yaml['topology_template']['policies']

                        with open(file, 'w') as tosca_file_out:
                            yaml.dump(tosca_yaml, tosca_file_out)
                    # current_app.logger.info("Processed", len(file_list), "tosca-files with 'drop_policies'.")
                else:
                    # traceback.print_stack(..)
                    current_app.logger.info("No tosca-files in", definitions_folder)
        else:
            current_app.logger.info("DropPolicies disabled, skipping.")

    @classmethod
    def get_parent_type(cls):
        return TestArtifact

    @classmethod
    def create(cls, testartifact_uuid):
        linked_testartifact = TestArtifact.get_by_uuid(testartifact_uuid)

        deployment = Deployment(linked_testartifact)
        deployment.deploy()

        # TODO: What to return here? Status of all deployments?
        return deployment

    @classmethod
    def get_all(cls):
        return Deployment.query.all()

    @classmethod
    def get_by_uuid(cls, get_uuid):
        return Deployment.query.filter_by(uuid=get_uuid).first()

    @classmethod
    def delete_by_uuid(cls, del_uuid):
        deployment = Deployment.query.filter_by(uuid=del_uuid)
        if deployment:
            from models.execution import Execution
            linked_executions = Execution.query.filter_by(deployment_uuid=del_uuid)
            for result in linked_executions:
                Execution.delete_by_uuid(result.uuid)

            deployment.delete()
            # rmtree(self.fq_storage_path)
            db_session.commit()
