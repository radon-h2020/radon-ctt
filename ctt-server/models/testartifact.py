import uuid
import os
from util.configuration import BasePath
from db_orm.database import Base, db_session
from sqlalchemy import Column, String, ForeignKey
from models.project import Project
from shutil import copytree, ignore_patterns
from sqlalchemy.orm import relationship, backref


class TestArtifact(Base):
    __tablename__ = 'testartifact'

    uuid: str
    commit_hash: str
    sut_tosca_path: str
    ti_tosca_path: str
    storage_path: str
    project_uuid: str

    uuid = Column(String, primary_key=True)
    commit_hash = Column(String, nullable=False)
    sut_tosca_path = Column(String, nullable=False)
    ti_tosca_path = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    project_uuid = Column(String, ForeignKey('project.uuid', ondelete='CASCADE'), nullable=False)
    project = relationship('Project', backref=backref('TestArtifact', passive_deletes=True))

    def __init__(self, project, sut_tosca_path, ti_tosca_path):
        self.uuid = str(uuid.uuid4())
        self.project_uuid = project.uuid
        self.sut_tosca_path = sut_tosca_path
        self.ti_tosca_path = ti_tosca_path
        self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)

        if not os.path.exists(self.fq_storage_path):
            os.makedirs(self.fq_storage_path)

        self.commit_hash = project.commit_hash

        # Copy repository excluding the '.git' directory
        src_dir = project.fq_storage_path
        if os.path.isdir(src_dir) and os.path.isdir(self.fq_storage_path):
            copytree(src_dir, self.fq_storage_path, ignore=ignore_patterns('.git'), dirs_exist_ok=True)

        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<TestArtifact UUID=%r, COMMIT_HASH=%r, SUT_PATH=%r, TI_PATH=%r, ST_PATH, PR_UUID=%r >' % \
               (self.uuid, self.commit_hash, self.sut_tosca_path, self.ti_tosca_path, self.storage_path, self.project_uuid)

    @property
    def fq_storage_path(self):
        return os.path.join(BasePath, self.storage_path)

    @classmethod
    def create_testartifact(cls, project_uuid, sut_tosca_path, ti_tosca_path):
        linked_project = Project.get_project_by_uuid(project_uuid)
        return TestArtifact(linked_project, sut_tosca_path, ti_tosca_path)

    @classmethod
    def get_testartifacts(cls):
        return TestArtifact.query.all()

    @classmethod
    def get_testartifact_by_uuid(cls, uuid):
        return TestArtifact.query.filter_by(uuid=uuid).first()

    @classmethod
    def delete_testartifact_by_uuid(cls, uuid):
        testartifact_to_delete = TestArtifact.query.filter_by(uuid=uuid)
        if testartifact_to_delete:
            # TODO: Delete depending items?!
            testartifact_to_delete.delete()
            db_session.commit()

        return testartifact_to_delete
