import connexion
import six

from openapi_server.models.result import Result  # noqa: E501
from openapi_server import util


def download_result_by_id(result_id):  # noqa: E501
    """Downloads the generated results

     # noqa: E501

    :param result_id: Id of result to download
    :type result_id: int

    :rtype: file
    """
    return 'do some magic!'


def get_result_by_id(result_id):  # noqa: E501
    """Retrieve a result

     # noqa: E501

    :param result_id: Id of Result to return
    :type result_id: int

    :rtype: Result
    """
    return 'do some magic!'


def get_results():  # noqa: E501
    """Get all results

     # noqa: E501


    :rtype: List[Result]
    """
    return 'do some magic!'
