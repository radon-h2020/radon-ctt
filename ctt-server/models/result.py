import uuid
import os
from util.configuration import StoragePath
from db_orm.database import Base
from sqlalchemy import Column, String, ForeignKey


class Result(Base):
    __tablename__ = 'result'

    uuid = Column(String, primary_key=True)
    storage_path = Column(String, nullable=False)
    project_uuid = Column(String, ForeignKey('project.uuid'), nullable=False)
    test_artifact_uuid = Column(String, ForeignKey('testartifact.uuid'), nullable=False)
    deployment_uuid = Column(String, ForeignKey('deployment.uuid'), nullable=False)
    execution_uuid = Column(String, ForeignKey('execution.uuid'), nullable=False)

    def __init__(self, project_uuid, test_artifact_uuid, deployment_uuid, execution_uuid):
        self.uuid = str(uuid.uuid4())
        self.project_uuid = project_uuid
        self.test_artifact_uuid = test_artifact_uuid
        self.deployment_uuid = deployment_uuid
        self.execution_uuid = execution_uuid
        self.storage_path = os.path.join(StoragePath, self.__tablename__, self.uuid)

    def __repr__(self):
        return '<Result UUID=%r, PR_UUID=%r, TA_UUID=%r, DP_UUID=%r, EX_UUID=%r, ST_PATH=%r>' % \
        (self.uuid, self.project_uuid, self.test_artifact_uuid, self.deployment_uuid, self.execution_uuid, self.storage_path)
