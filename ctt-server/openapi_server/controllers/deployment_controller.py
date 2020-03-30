import connexion
import six

from openapi_server.models.deployment import Deployment  # noqa: E501
from openapi_server.models.post_deployment import POSTDeployment  # noqa: E501
from openapi_server import util

from models.deployment import Deployment as DeploymentImpl
from util.marhsmallow_schemas import DeploymentSchema

deployment_schema = DeploymentSchema()
deployment_schema_many = DeploymentSchema(many=True)


def create_deployment(post_deployment=None):  # noqa: E501
    """Creates a deployment

     # noqa: E501

    :param post_deployment:
    :type post_deployment: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_deployment = POSTDeployment.from_dict(connexion.request.get_json())  # noqa: E501
    created_deployment = DeploymentImpl.create(post_deployment.testartifact_uuid)
    return deployment_schema.dump(created_deployment)


def delete_deployment_by_uuid(deployment_uuid):  # noqa: E501
    """Delete a deployment

    Deletes the test artifact with the given UUID and all elements depending on it # noqa: E501

    :param deployment_uuid: UUID of the deployment to delete
    :type deployment_uuid: str

    :rtype: Deployment
    """
    deployment = DeploymentImpl.delete_by_uuid(deployment_uuid)
    return deployment_schema.dump(deployment)


def get_deployment_by_uuid(deployment_uuid):  # noqa: E501
    """Retrieve a deployment

     # noqa: E501

    :param deployment_uuid: UUID of the deployment to return
    :type deployment_uuid: str

    :rtype: Deployment
    """
    deployment = DeploymentImpl.get_by_uuid(deployment_uuid)
    return deployment_schema.dump(deployment)


def get_deployments():  # noqa: E501
    """Get all deployments

     # noqa: E501


    :rtype: List[Deployment]
    """
    deployments = DeploymentImpl.get_all()
    return deployment_schema_many.dump(deployments)
