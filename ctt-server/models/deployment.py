import opera
import os
import subprocess
import uuid

from flask import current_app
from sqlalchemy import Column, String, ForeignKey

from db_orm.database import Base, db_session
from models.testartifact import TestArtifact
from models.abstract_model import AbstractModel


class Deployment(Base, AbstractModel):
    __tablename__ = 'deployment'

    uuid: str
    testartifact_uuid: str
    status: str

    uuid = Column(String, primary_key=True)
    testartifact_uuid = Column(String, ForeignKey('testartifact.uuid'), nullable=False)

    def __init__(self, testartifact):
        self.uuid = str(uuid.uuid4())
        self.testartifact_uuid = testartifact.uuid
        if testartifact:
            db_session.add(self)
            db_session.commit()
        else:
            raise Exception(f'Linked entities do not exist.')

    def __repr__(self):
        return '<Deployment UUID=%r, TA_UUID=%r>' % (self.uuid, self.testartifact_uuid)

    def deploy(self):
        test_artifact = TestArtifact.get_by_uuid(self.testartifact_uuid)
        sut_fq_path = os.path.join(test_artifact.fq_storage_path, test_artifact.sut_tosca_path)
        ti_fq_path = os.path.join(test_artifact.fq_storage_path, test_artifact.ti_tosca_path)

        # Deployment of SuT
        if os.path.isfile(sut_fq_path):
            current_app.logger.debug(f'Deploying SuT {str(test_artifact.sut_tosca_path)} with opera '
                                     f'in folder {str(test_artifact.fq_storage_path)}.')
            subprocess.call(['opera', 'deploy', test_artifact.sut_tosca_path], cwd=test_artifact.fq_storage_path)

        # Deployment of TI
        if os.path.isfile(ti_fq_path):
            current_app.logger.debug(f'Deploying TI {str(test_artifact.ti_tosca_path)} with opera '
                                     f'in folder {str(test_artifact.fq_storage_path)}.')
            subprocess.call(['opera', 'deploy', test_artifact.ti_tosca_path], cwd=test_artifact.fq_storage_path)

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
