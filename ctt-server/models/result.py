import uuid
import os
from util.configuration import BasePath
from db_orm.database import Base, db_session
from sqlalchemy import Column, String, ForeignKey
from models.execution import Execution


class Result(Base):
    __tablename__ = 'result'

    uuid: str
    storage_path: str
    execution_uuid: str

    uuid = Column(String, primary_key=True)
    storage_path = Column(String, nullable=False)
    execution_uuid = Column(String, ForeignKey('execution.uuid'), nullable=False)

    def __init__(self, execution):
        self.uuid = str(uuid.uuid4())
        self.execution_uuid = execution.uuid
        self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)

        self.fq_storage_path = os.path.join(BasePath, self.storage_path)

        if execution:
            db_session.add(self)
            db_session.commit()
        else:
            raise Exception(f'Linked entities do not exist.')

    def __repr__(self):
        return '<Result UUID=%r, PR_UUID=%r, TA_UUID=%r, DP_UUID=%r, EX_UUID=%r, ST_PATH=%r>' % \
        (self.uuid, self.execution_uuid, self.storage_path)

    @property
    def fq_storage_path(self):
        return self.fq_storage_path

    @classmethod
    def create_result(cls, execution_uuid):
        linked_execution = Execution.get_execution_by_uuid(execution_uuid)
        result = Result(linked_execution)
        return result

    @classmethod
    def get_results(cls):
        return Result.query.all()

    @classmethod
    def get_result_by_uuid(cls, uuid):
        return Result.query.filter_by(uuid=uuid).first()


