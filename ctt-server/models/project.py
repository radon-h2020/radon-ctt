import git

from flask import current_app
from os import getenv, makedirs, path
from shutil import copytree, rmtree
from sqlalchemy import Boolean, Column, String

from db_orm.database import Base, db_session
from models.abstract_model import AbstractModel
from util.configuration import is_che_env, get_dir_prefix, get_path


class Project(Base, AbstractModel):
    """
    * Create Project
        - clones the given repository if the given name does not exist yet,
        - otherwise it pulls the latest version
    """
    __tablename__ = 'project'

    uuid: str
    name: str
    repository_url: str
    storage_path: str
    che_env: bool

    uuid = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    repository_url = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    che_env = Column(Boolean, nullable=False)

    def __init__(self, uuid, name, repository_url, storage_path):
        self.uuid = uuid
        self.name = name
        self.repository_url = repository_url
        self.storage_path = storage_path
        self.che_env = is_che_env()

        current_app.logger.info(f"CHE environment: {self.che_env}")

        if not path.exists(self.fq_storage_path):
            makedirs(self.fq_storage_path)
            current_app.logger.info(f"Created directory path {self.fq_storage_path}")

        if self.che_env:
            src_path = path.join(get_dir_prefix(), self.repository_url)
            current_app.logger.info(f'Copying directory tree from  {src_path} into {self.fq_storage_path}')
            copytree(src_path, self.fq_storage_path, dirs_exist_ok=True)
        else:
            current_app.logger.info(f'Cloning repository {self.repository_url} into {self.fq_storage_path}')
            git.Git(self.fq_storage_path).clone(self.repository_url, self.fq_storage_path)

        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<Project %r, %r, %r, %r>' % (self.uuid, self.name, self.repository_url, self.storage_path)

    @property
    def commit_hash(self):
        if self.che_env:
            return "che-mode_no-hash-available"
        else:
            return git.Repo(self.fq_storage_path).head.commit.hexsha

    @property
    def repository_src_url(self):
        return self.repository_url

    @property
    def is_che_project(self):
        return self.che_env

    @property
    def fq_storage_path(self):
        return path.join(get_path(), self.storage_path)

    @classmethod
    def get_parent_type(cls):
        return None

    @classmethod
    def create(cls, name, repository_url):
        # New Project
        if not Project.exists(name):
            import uuid
            new_uuid = str(uuid.uuid4())
            new_storage_path = path.join(Project.__tablename__, new_uuid)
            project = Project(new_uuid, name, repository_url, new_storage_path)
            current_app.logger.info('Project created: ' + str(project))

        # Existing Project
        else:
            project = Project.query.filter_by(name=name).first()
            if project.is_che_project:
                copytree(path.join(get_dir_prefix(), project.repository_src_url), path.join(get_path(), project.storage_path), dirs_exist_ok=True)
            else:
                git.Git(path.join(get_path(), project.storage_path)).pull()
            current_app.logger.info(f"Project {str(project)} updated.")

        return project

    @classmethod
    def get_all(cls):
        return Project.query.all()

    @classmethod
    def get_by_uuid(cls, get_uuid):
        return Project.query.filter_by(uuid=get_uuid).first()

    @classmethod
    def exists(cls, name):
        if Project.query.filter_by(name=name).count() > 0:
            return True
        else:
            return False

    @classmethod
    def delete_by_uuid(cls, del_uuid):
        project = Project.query.filter_by(uuid=del_uuid)
        if project:
            folder_to_delete = project.first().fq_storage_path
            from models.testartifact import TestArtifact
            linked_testartifacts = TestArtifact.query.filter_by(project_uuid=del_uuid)
            for result in linked_testartifacts:
                TestArtifact.delete_by_uuid(result.uuid)
            project.delete()
            rmtree(folder_to_delete)
            db_session.commit()
