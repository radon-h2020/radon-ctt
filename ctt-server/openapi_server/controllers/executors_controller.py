import connexion
import six

from openapi_server.models.executor import Executor  # noqa: E501
from openapi_server.models.post_executors import POSTExecutors  # noqa: E501
from openapi_server import util


def create_executor(post_executors=None):  # noqa: E501
    """Creates an executor

     # noqa: E501

    :param post_executors: 
    :type post_executors: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_executors = POSTExecutors.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_executor_by_id(executor_id):  # noqa: E501
    """Retrieve an executor

     # noqa: E501

    :param executor_id: ID of the executor to return
    :type executor_id: int

    :rtype: Executor
    """
    return 'do some magic!'


def get_executors():  # noqa: E501
    """Get all executors

     # noqa: E501


    :rtype: List[Executor]
    """
    return 'do some magic!'
