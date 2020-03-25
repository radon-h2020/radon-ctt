import uuid
from db_orm.database import Base, db_session
from sqlalchemy import Column, String, ForeignKey
from models.project import Project
from models.testartifact import TestArtifact


class Deployment(Base):
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
    def create_deployment(cls, testartifact_uuid):
        linked_testartifact = TestArtifact.get_testartifact_by_uuid(testartifact_uuid)

        deployment = Deployment(linked_testartifact)
        deployment.deploy_sut()
        deployment.deploy_ti()

        # TODO: What to return here? Status of all deployments?
        return deployment

    @classmethod
    def get_deployments(cls):
        return Deployment.query.all()

    @classmethod
    def get_deployment_by_uuid(cls, uuid):
        return Deployment.query.filter_by(uuid=uuid).first()

    @classmethod
    def delete_deployment_by_uuid(cls, uuid):
        deployment_to_delete = Deployment.query.filter_by(uuid=uuid)
        if deployment_to_delete:
            # TODO: Delete depending items?!
            Deployment.delete(deployment_to_delete)
            db_session.commit()

        return deployment_to_delete
