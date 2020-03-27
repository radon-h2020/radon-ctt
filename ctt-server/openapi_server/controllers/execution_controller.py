import connexion
import six

from openapi_server.models.execution import Execution  # noqa: E501
from openapi_server.models.post_execution import POSTExecution  # noqa: E501
from openapi_server import util

from models.execution import Execution as ExecutionImpl
from util.marhsmallow_schemas import ExecutionSchema

execution_schema = ExecutionSchema()
execution_schema_many = ExecutionSchema(many=True)


def create_execution(post_execution=None):  # noqa: E501
    """Creates an execution

     # noqa: E501

    :param post_execution:
    :type post_execution: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_execution = POSTExecution.from_dict(connexion.request.get_json())  # noqa: E501

    created_execution = ExecutionImpl.create(post_execution.deployment_uuid)
    return execution_schema.dump(created_execution)


def delete_execution_by_uuid(execution_uuid):  # noqa: E501
    """Delete an execution

    Deletes the execution with the given UUID and all elements depending on it # noqa: E501

    :param execution_uuid: UUID of the execution to delete
    :type execution_uuid: str

    :rtype: Execution
    """
    execution = ExecutionImpl.delete_by_uuid(execution_uuid)
    return execution_schema.dump(execution)


def get_execution_by_uuid(execution_uuid):  # noqa: E501
    """Retrieve an execution

     # noqa: E501

    :param execution_uuid: UUID of the execution to return
    :type execution_uuid: str

    :rtype: Execution
    """
    execution = ExecutionImpl.get_by_uuid(execution_uuid)
    return execution_schema.dump(execution)


def get_executions():  # noqa: E501
    """Get all executions

     # noqa: E501


    :rtype: List[Execution]
    """
    executions = ExecutionImpl.get_all()
    return execution_schema_many.dump(executions)
