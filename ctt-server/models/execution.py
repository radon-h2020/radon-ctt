import uuid
import os
from util.configuration import StoragePath
from db_orm.database import Base
from sqlalchemy import Column, String, ForeignKey


class Execution(Base):
    __tablename__ = 'execution'

    uuid = Column(String, primary_key=True)
    project_uuid = Column(String, ForeignKey('project.uuid'), nullable=False)
    deployment_uuid = Column(String, ForeignKey('deployment.uuid'), nullable=False)

    def __init__(self, project_uuid, deployment_uuid):
        self.uuid = str(uuid.uuid4())
        self.project_uuid = project_uuid
        self.deployment_uuid = deployment_uuid

    def __repr__(self):
        return '<Execution UUID=%r, PR_UUID=%r, DP_UUID=%r>' % (self.uuid, self.project_uuid, self.deployment_uuid)

