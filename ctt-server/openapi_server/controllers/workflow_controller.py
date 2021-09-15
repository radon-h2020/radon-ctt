import connexion
import six

from openapi_server.models.execution import Execution  # noqa: E501
from openapi_server.models.post_workflow import POSTWorkflow  # noqa: E501
from openapi_server import util

from models.workflow import Workflow as WorkflowImpl
from util.marshmallow_schemas import WorkflowSchema

workflow_schema = WorkflowSchema()
workflow_schema_many = WorkflowSchema(many=True)


def create_workflow(body=None):  # noqa: E501
    """Creates a workflow

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    created_workflow = WorkflowImpl.create(body)
    # return workflow_schema.dump(created_workflow)
    return created_workflow
