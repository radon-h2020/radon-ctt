import git
import os
from util.configuration import BasePath
from db_orm.database import Base, db_session
from sqlalchemy import Column, String


class Project(Base):
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

    uuid = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    repository_url = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)

    def __init__(self, uuid, name, repository_url, storage_path):
        self.uuid = uuid
        self.name = name
        self.repository_url = repository_url
        self.storage_path = storage_path

        if not os.path.exists(self.fq_storage_path):
            os.makedirs(self.fq_storage_path)

        git.Git(self.fq_storage_path).\
            clone(self.repository_url, self.fq_storage_path)

        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<Project %r, %r, %r, %r>' % (self.uuid, self.name, self.repository_url, self.storage_path)

    @property
    def commit_hash(self):
        return git.Repo(self.fq_storage_path).head.commit.hexsha

    @property
    def fq_storage_path(self):
        return os.path.join(BasePath, self.storage_path)

    @classmethod
    def create_project(cls, name, repository_url):

        # New Project
        if not Project.exists(name):
            import uuid
            new_uuid = str(uuid.uuid4())
            new_storage_path = os.path.join(Project.__tablename__, new_uuid)
            project = Project(new_uuid, name, repository_url, new_storage_path)
            print("Created new project", project)

        # Existing Project
        else:
            project = Project.query.filter_by(name=name).first()
            git.Git(os.path.join(BasePath, project.storage_path)).pull()
            print("Updated project", project)

        return project

    @classmethod
    def get_projects(cls):
        return Project.query.all()

    @classmethod
    def get_project_by_uuid(cls, uuid):
        return Project.query.filter_by(uuid=uuid).first()

    @classmethod
    def exists(cls, name):
        if Project.query.filter_by(name=name).count() > 0:
            return True
        else:
            return False

    @classmethod
    def delete_project_by_uuid(cls, uuid):
        project_to_delete = Project.query.filter_by(uuid=uuid)
        if project_to_delete:
            # TODO: Delete depending items?!
            Project.delete(project_to_delete)
            db_session.commit()

        return project_to_delete