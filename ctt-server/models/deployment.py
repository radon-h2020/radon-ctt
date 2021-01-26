import os
import re
import subprocess
import time
import uuid
import yaml

from flask import current_app
from sqlalchemy import Column, String, ForeignKey
from opera.error import OperationError

from db_orm.database import Base, db_session
from models.testartifact import TestArtifact
from models.abstract_model import AbstractModel
from util.configuration import get_path, DropPolicies, is_test_mode
from util.tosca_helper import Csar

ip_pattern = re.compile('([1][0-9][0-9].|^[2][5][0-5].|^[2][0-4][0-9].|^[1][0-9][0-9].|^[0-9][0-9].|^[0-9].)'
                        '([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)'
                        '([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)'
                        '([1][0-9][0-9]|[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[0-9][0-9]|[0-9])')


class Deployment(Base, AbstractModel):
    __tablename__ = 'deployment'

    uuid: str
    testartifact_uuid: str
    storage_path: str
    status: str
    sut_hostname: str
    ti_hostname: str

    uuid = Column(String, primary_key=True)
    testartifact_uuid = Column(String, ForeignKey('testartifact.uuid'), nullable=False)
    sut_hostname = Column(String)
    ti_hostname = Column(String)

    def __init__(self, testartifact):
        self.uuid = str(uuid.uuid4())
        self.testartifact_uuid = testartifact.uuid
        self.storage_path = os.path.join(get_path(), self.__tablename__, self.uuid)
        self.__test_artifact = testartifact
        self.sut_hostname = 'localhost'
        self.ti_hostname = 'localhost'

        if testartifact:
            db_session.add(self)
            db_session.commit()
        else:
            raise Exception(f'Linked entities do not exist.')

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def __repr__(self):
        return '<Deployment UUID=%r, TA_UUID=%r>' % (self.uuid, self.testartifact_uuid)

    @property
    def hostname_sut(self):
        return self.sut_hostname

    @property
    def hostname_ti(self):
        return self.ti_hostname

    def deploy(self):
        test_artifact = TestArtifact.get_by_uuid(self.testartifact_uuid)
        sut_csar_path = os.path.join(test_artifact.fq_storage_path, test_artifact.sut_tosca_path)
        ti_csar_path = os.path.join(test_artifact.fq_storage_path, test_artifact.ti_tosca_path)

        if test_artifact.sut_inputs_path:
            sut_inputs_path = os.path.join(test_artifact.fq_storage_path, test_artifact.sut_inputs_path)
        else:
            sut_inputs_path = None

        if test_artifact.ti_inputs_path:
            ti_inputs_path = os.path.join(test_artifact.fq_storage_path, test_artifact.ti_inputs_path)
        else:
            ti_inputs_path = None

        # Deployment of SuT
        with Csar(sut_csar_path, extract_dir=self.sut_storage_path, keep=True) as sut_csar:
            if DropPolicies:
                sut_csar.drop_policies()
            entry_definition = sut_csar.tosca_entry_point

            current_app.logger.\
                info(f'Deploying SuT {str(entry_definition)} with opera in folder {str(self.sut_storage_path)}.')

            if not is_test_mode():
                try:
                    if sut_inputs_path:
                        subprocess.call(['opera', 'deploy',
                                         '-p', self.sut_storage_path,
                                         '-i', sut_inputs_path,
                                         entry_definition],
                                        cwd=self.sut_storage_path)
                    else:
                        subprocess.call(['opera', 'deploy',
                                         '-p', self.sut_storage_path,
                                         entry_definition],
                                        cwd=self.sut_storage_path)
                    opera_outputs = subprocess.check_output(['opera', 'outputs',
                                                             '-p', self.sut_storage_path],
                                                            cwd=self.sut_storage_path)
                    current_app.logger.info(f'Opera returned output {opera_outputs}.')
                except OperationError:
                    subprocess.call(['opera', 'undeploy',
                                     '-p', self.sut_storage_path])

        # Deployment of TI
        with Csar(ti_csar_path, extract_dir=self.ti_storage_path, keep=True) as ti_csar:
            if DropPolicies:
                ti_csar.drop_policies()
            entry_definition = ti_csar.tosca_entry_point

            if entry_definition:
                current_app.logger.\
                    info(f'Deploying TI {str(entry_definition)} with opera in folder {str(self.ti_storage_path)}.')

                if not is_test_mode():
                    try:
                        if ti_inputs_path:
                            subprocess.call(['opera', 'deploy',
                                             '-p', self.ti_storage_path,
                                             '-i', ti_inputs_path,
                                             entry_definition],
                                            cwd=self.ti_storage_path)
                        else:
                            subprocess.call(['opera', 'deploy',
                                             '-p', self.ti_storage_path,
                                             entry_definition],
                                            cwd=self.ti_storage_path)
                        opera_outputs = subprocess.check_output(['opera', 'outputs',
                                                                 '-p', self.ti_storage_path],
                                                                cwd=self.ti_storage_path)
                        current_app.logger.info(f'Opera returned output {opera_outputs}.')
                        opera_yaml_outputs = yaml.safe_load(opera_outputs)
                        time.sleep(30)
                    except OperationError:
                        subprocess.call(['opera', 'undeploy',
                                         '-p', self.ti_storage_path])

                    self.sut_hostname = self.__test_artifact.policy_yaml['properties']['hostname']
                    current_app.logger.info(f'SUT hostname {self.sut_hostname}.')

                    self.ti_hostname = opera_yaml_outputs['public_address']['value']
                    current_app.logger.info(f'TI hostname {self.ti_hostname}.')

        db_session.add(self)
        db_session.commit()

    def undeploy(self):
        if not is_test_mode():
            subprocess.call(['opera', 'undeploy', '-p', self.sut_storage_path], cwd=self.sut_storage_path)
            subprocess.call(['opera', 'undeploy', '-p', self.ti_storage_path], cwd=self.ti_storage_path)

    def get_uuid(self):
        return self.uuid

    @property
    def base_storage_path(self):
        return self.storage_path

    @property
    def sut_storage_path(self):
        return os.path.join(self.storage_path, 'system_under_test')

    @property
    def ti_storage_path(self):
        return os.path.join(self.storage_path, 'test_infrastructure')

    @property
    def test_artifact(self):
        return TestArtifact.get_by_uuid(self.testartifact_uuid)

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
        result = Deployment.query.filter_by(uuid=get_uuid).first()

        if result:
            return result
        else:
            error_msg = f'{cls.__name__} with UUID {get_uuid} could not be found.'
            current_app.logger.error(error_msg)
            raise LookupError(error_msg)

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
