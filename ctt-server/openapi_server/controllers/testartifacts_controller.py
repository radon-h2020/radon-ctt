import connexion
import six

from openapi_server.models.post_testartifacts import POSTTestartifacts  # noqa: E501
from openapi_server.models.testartifact import Testartifact  # noqa: E501
from openapi_server import util


def create_testartifact(post_testartifacts=None):  # noqa: E501
    """Creates a test artifact

     # noqa: E501

    :param post_testartifacts: 
    :type post_testartifacts: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_testartifacts = POSTTestartifacts.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def download_testartifact_by_id(testartifact_id):  # noqa: E501
    """Downloads the generated test artifact

     # noqa: E501

    :param testartifact_id: ID of the test artifact to download
    :type testartifact_id: int

    :rtype: file
    """
    return 'do some magic!'


def get_testartifact_by_id(testartifact_id):  # noqa: E501
    """Retrieve a test artifact

     # noqa: E501

    :param testartifact_id: ID of the test artifact to return
    :type testartifact_id: int

    :rtype: Testartifact
    """
    return 'do some magic!'


def get_testartifacts():  # noqa: E501
    """Get all test artifacts

     # noqa: E501


    :rtype: List[Testartifact]
    """
    return 'do some magic!'
