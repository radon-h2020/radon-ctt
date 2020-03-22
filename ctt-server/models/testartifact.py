import uuid
import os
from util.configuration import StoragePath
from db_orm.database import Base
from sqlalchemy import Column, String, ForeignKey


class TestArtifact(Base):
    __tablename__ = 'testartifact'

    uuid = Column(String, primary_key=True)
    storage_path = Column(String, nullable=False)
    project_uuid = Column(String, ForeignKey('project.uuid'), nullable=False)

    def __init__(self, project_uuid):
        self.uuid = str(uuid.uuid4())
        self.project_uuid = project_uuid
        self.storage_path = os.path.join(StoragePath, self.__tablename__, self.uuid)

    def __repr__(self):
        return '<TestArtifact UUID=%r, PR_UUID=%r ST_PATH=%r>' % (self.uuid, self.project_uuid, self.storage_path)
