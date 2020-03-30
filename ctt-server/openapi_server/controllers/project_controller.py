import connexion
import six

from openapi_server.models.post_project import POSTProject  # noqa: E501
from openapi_server.models.project import Project  # noqa: E501
from openapi_server import util

from models.project import Project as ProjectImpl
from util.marhsmallow_schemas import ProjectSchema

project_schema = ProjectSchema()
project_schema_many = ProjectSchema(many=True)


def create_project(post_project=None):  # noqa: E501
    """Creates a project

     # noqa: E501

    :param post_project:
    :type post_project: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_project = POSTProject.from_dict(connexion.request.get_json())  # noqa: E501

    created_project = ProjectImpl.create(post_project.name, post_project.repository_url)
    return project_schema.dump(created_project)


def delete_project(project_uuid):  # noqa: E501
    """Delete a project

     # noqa: E501

    :param project_uuid: UUID of the project to delete
    :type project_uuid: str

    :rtype: None
    """
    deleted_project = ProjectImpl.delete_by_uuid(project_uuid)
    return project_schema.dump(deleted_project)


def get_project_by_uuid(project_uuid):  # noqa: E501
    """Retrieve a project

     # noqa: E501

    :param project_uuid: UUID of the project to return
    :type project_uuid: str

    :rtype: Project
    """
    project = ProjectImpl.get_by_uuid(project_uuid)
    return project_schema.dump(project)


def get_projects():  # noqa: E501
    """Get a list of all projects

     # noqa: E501


    :rtype: List[Project]
    """
    projects = ProjectImpl.get_all()
    return project_schema_many.dump(projects)
