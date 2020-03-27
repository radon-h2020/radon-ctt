import uuid
import os

from sqlalchemy import Column, String, ForeignKey
from shutil import copytree, ignore_patterns, rmtree

from util.configuration import BasePath
from db_orm.database import Base, db_session
from models.project import Project
from models.model_interface import AbstractModel


class TestArtifact(Base, AbstractModel):
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
    project_uuid = Column(String, ForeignKey('project.uuid'), nullable=False)

    parentType = Project

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
    def get_parent_type(cls):
        return Project

    @classmethod
    def create(cls, project_uuid, sut_tosca_path, ti_tosca_path):
        linked_project = Project.get_by_uuid(project_uuid)
        return TestArtifact(linked_project, sut_tosca_path, ti_tosca_path)

    @classmethod
    def get_all(cls):
        return TestArtifact.query.all()

    @classmethod
    def get_by_uuid(cls, uuid):
        return TestArtifact.query.filter_by(uuid=uuid).first()

    @classmethod
    def delete_by_uuid(cls, uuid):
        testartifact = TestArtifact.query.filter_by(uuid=uuid)
        if testartifact:
            folder_to_delete = testartifact.first().fq_storage_path
            from models.deployment import Deployment
            linked_deployments = Deployment.query.filter_by(testartifact_uuid=uuid)
            for result in linked_deployments:
                Deployment.delete_by_uuid(result.uuid)
            testartifact.delete()
            rmtree(folder_to_delete)
            db_session.commit()
