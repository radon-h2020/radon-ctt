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
from util.tosca_helper import Csar


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

        # Deployment of SuT
        with Csar(sut_csar_path, extract_dir=self.sut_storage_path, keep=True) as sut_csar:
            if DropPolicies:
                sut_csar.drop_policies()
            entry_definition = sut_csar.tosca_entry_point

            current_app.logger.\
                info(f'Deploying SuT {str(entry_definition)} with opera in folder {str(self.sut_storage_path)}.')
            subprocess.call(['opera', 'deploy', entry_definition], cwd=self.sut_storage_path)

        # Deployment of TI
        with Csar(ti_csar_path, extract_dir=self.ti_storage_path, keep=True) as ti_csar:
            if DropPolicies:
                ti_csar.drop_policies()
            entry_definition = ti_csar.tosca_entry_point

            if entry_definition:
                current_app.logger.\
                    info(f'Deploying TI {str(entry_definition)} with opera in folder {str(self.ti_storage_path)}.')
                subprocess.call(['opera', 'deploy', entry_definition], cwd=self.ti_storage_path)

    def undeploy(self):
        subprocess.call(['opera', 'undeploy'], cwd=self.sut_storage_path)
        subprocess.call(['opera', 'undeploy'], cwd=self.ti_storage_path)

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
