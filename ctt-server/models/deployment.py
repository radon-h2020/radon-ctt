import uuid

from flask import current_app
from sqlalchemy import Column, String, ForeignKey

from db_orm.database import Base, db_session
from models.testartifact import TestArtifact
from models.model_interface import AbstractModel


class Deployment(Base, AbstractModel):
    __tablename__ = 'deployment'

    uuid: str
    testartifact_uuid: str

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

    def deploy_sut(self):
        pass

    def deploy_ti(self):
        pass

    @classmethod
    def get_parent_type(cls):
        return TestArtifact

    @classmethod
    def create(cls, testartifact_uuid):
        linked_testartifact = TestArtifact.get_by_uuid(testartifact_uuid)

        deployment = Deployment(linked_testartifact)
        deployment.deploy_sut()
        deployment.deploy_ti()

        # TODO: What to return here? Status of all deployments?
        return deployment

    @classmethod
    def get_all(cls):
        return Deployment.query.all()

    @classmethod
    def get_by_uuid(cls, uuid):
        return Deployment.query.filter_by(uuid=uuid).first()

    @classmethod
    def delete_by_uuid(cls, uuid):
        deployment = Deployment.query.filter_by(uuid=uuid)
        if deployment:
            from models.execution import Execution
            linked_executions = Execution.query.filter_by(deployment_uuid=uuid)
            for result in linked_executions:
                Execution.delete_by_uuid(result.uuid)

            deployment.delete()
            # rmtree(self.fq_storage_path)
            db_session.commit()
