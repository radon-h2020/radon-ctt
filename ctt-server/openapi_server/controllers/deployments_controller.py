import connexion
import six

from openapi_server.models.deployment import Deployment  # noqa: E501
from openapi_server.models.post_deployments import POSTDeployments  # noqa: E501
from openapi_server import util


def create_deployment(post_deployments=None):  # noqa: E501
    """Creates a deployment

     # noqa: E501

    :param post_deployments: 
    :type post_deployments: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_deployments = POSTDeployments.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_deployment_by_id(deployment_id):  # noqa: E501
    """Retrieve a deployment

     # noqa: E501

    :param deployment_id: Id of deployment to return
    :type deployment_id: int

    :rtype: Deployment
    """
    return 'do some magic!'


def get_deployments():  # noqa: E501
    """Get all deployments

     # noqa: E501


    :rtype: List[Deployment]
    """
    return 'do some magic!'
