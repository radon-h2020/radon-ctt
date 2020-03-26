import uuid
import os

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from db_orm.database import Base, db_session
from models.deployment import Deployment
from util.configuration import BasePath


class Execution(Base):
    __tablename__ = 'execution'

    uuid = Column(String, primary_key=True)
    deployment_uuid = Column(String, ForeignKey('deployment.uuid'), nullable=False)
    deployment = relationship('Deployment', backref=backref('Execution', passive_deletes=True))

    def __init__(self, deployment):
        self.uuid = str(uuid.uuid4())
        self.deployment_uuid = deployment.uuid
        self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)

        if deployment:
            db_session.add(self)
            db_session.commit()
        else:
            raise Exception(f'Linked entities do not exist.')

    def __repr__(self):
        return '<Execution UUID=%r, DP_UUID=%r>' % (self.uuid, self.deployment_uuid)

    def run(self):
        pass

    @classmethod
    def create_execution(cls, deployment_uuid):
        linked_deployment = Deployment.get_deployment_by_uuid(deployment_uuid)
        execution = Execution(linked_deployment)
        execution.run()
        return execution

    @classmethod
    def get_executions(cls):
        return Execution.query.all()

    @classmethod
    def get_execution_by_uuid(cls, uuid):
        return Execution.query.filter_by(uuid=uuid).first()

    @classmethod
    def delete_execution_by_uuid(cls, uuid):
        execution_to_delete = Execution.query.filter_by(uuid=uuid)
        if execution_to_delete:
            # TODO: Delete depending items?!
            execution_to_delete.delete()
            db_session.commit()

        return execution_to_delete
