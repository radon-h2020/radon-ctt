import connexion
import six

from openapi_server.models.post_projects import POSTProjects  # noqa: E501
from openapi_server.models.project import Project  # noqa: E501
from openapi_server import util


def create_project(post_projects=None):  # noqa: E501
    """Creates a project

     # noqa: E501

    :param post_projects: 
    :type post_projects: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_projects = POSTProjects.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_project(project_id):  # noqa: E501
    """Delete a project

     # noqa: E501

    :param project_id: Id of project to delete
    :type project_id: int

    :rtype: None
    """
    return 'do some magic!'


def get_project_by_id(project_id):  # noqa: E501
    """Retrieve a project

     # noqa: E501

    :param project_id: Id of project to return
    :type project_id: int

    :rtype: Project
    """
    return 'do some magic!'


def get_projects():  # noqa: E501
    """Get a list of projects

     # noqa: E501


    :rtype: List[Project]
    """
    return 'do some magic!'
