import uuid
import os
from util.configuration import StoragePath
from db_orm.database import Base
from sqlalchemy import Column, Integer, String


class Project(Base):
    __tablename__ = 'project'

    uuid = Column(String, primary_key=True)
    repository_url = Column(String, nullable=False, unique=True)
    sut_tosca_path = Column(String, nullable=False)
    ti_tosca_path = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)

    def __init__(self, repository_url, sut_tosca_path, ti_tosca_path):
        self.uuid = str(uuid.uuid4())
        self.repository_url = repository_url
        self.sut_tosca_path = sut_tosca_path
        self.ti_tosca_path = ti_tosca_path
        self.storage_path = os.path.join(StoragePath, self.__tablename__, self.uuid)

    def __repr__(self):
        return '<Project %r, %r, %r, %r, %r>' % (self.uuid, self.repository_url, self.sut_tosca_path, self.ti_tosca_path, self.storage_path)
