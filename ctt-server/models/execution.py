import uuid
import os

from sqlalchemy import Column, String, ForeignKey

from db_orm.database import Base, db_session
from models.deployment import Deployment
from models.abstract_model import AbstractModel
from util.configuration import BasePath


class Execution(Base, AbstractModel):
    __tablename__ = 'execution'

    uuid: str
    deployment_uuid: str

    uuid = Column(String, primary_key=True)
    deployment_uuid = Column(String, ForeignKey('deployment.uuid'), nullable=False)

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
    def get_parent_type(cls):
        return Deployment

    @classmethod
    def create(cls, deployment_uuid):
        linked_deployment = Deployment.get_by_uuid(deployment_uuid)
        execution = Execution(linked_deployment)
        execution.run()
        return execution

    @classmethod
    def get_all(cls):
        return Execution.query.all()

    @classmethod
    def get_by_uuid(cls, get_uuid):
        return Execution.query.filter_by(uuid=get_uuid).first()

    @classmethod
    def delete_by_uuid(cls, del_uuid):
        execution = Execution.query.filter_by(uuid=del_uuid)
        if execution:
            from models.result import Result
            linked_results = Result.query.filter_by(execution_uuid=del_uuid)
            for result in linked_results:
                Result.delete_by_uuid(result.uuid)
            execution.delete()
            # rmtree(self.fq_storage_path)
            db_session.commit()
