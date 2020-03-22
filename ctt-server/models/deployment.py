import uuid
import os
from util.configuration import StoragePath
from db_orm.database import Base
from sqlalchemy import Column, String, ForeignKey


class Deployment(Base):
    __tablename__ = 'deployment'

    uuid = Column(String, primary_key=True)
    project_uuid = Column(String, ForeignKey('project.uuid'), nullable=False)
    test_artifact_uuid = Column(String, ForeignKey('testartifact.uuid'), nullable=False)

    def __init__(self, project_uuid, test_artifact_uuid):
        self.uuid = str(uuid.uuid4())
        self.project_uuid = project_uuid
        self.test_artifact_uuid = test_artifact_uuid

    def __repr__(self):
        return '<Deployment UUID=%r, PR_UUID=%r, TA_UUID=%r>' % (self.uuid, self.project_uuid, self.test_artifact_uuid)
