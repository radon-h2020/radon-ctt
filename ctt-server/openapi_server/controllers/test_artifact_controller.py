import connexion
import six

from openapi_server.models.post_test_artifact import POSTTestArtifact  # noqa: E501
from openapi_server.models.test_artifact import TestArtifact  # noqa: E501
from openapi_server import util

from models.testartifact import TestArtifact as TestArtifactImpl
from util.marhsmallow_schemas import TestArtifactSchema

testartifact_schema = TestArtifactSchema()
testartifact_schema_many = TestArtifactSchema(many=True)


def create_testartifact(post_test_artifact=None):  # noqa: E501
    """Creates a test artifact

     # noqa: E501

    :param post_test_artifact:
    :type post_test_artifact: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_testartifact = POSTTestArtifact.from_dict(connexion.request.get_json())  # noqa: E501

    created_testartifacts = TestArtifactImpl.create_testartifact(
        post_testartifact.project_uuid, post_testartifact.sut_tosca_path, post_testartifact.ti_tosca_path)
    return testartifact_schema.dump(created_testartifacts)


def download_testartifact_by_uuid(testartifact_uuid):  # noqa: E501
    """Downloads the generated test artifact

     # noqa: E501

    :param testartifact_uuid: UUID of the test artifact to download
    :type testartifact_uuid: str

    :rtype: file
    """
    raise Exception('Not Implemented')


def get_testartifact_by_uuid(testartifact_uuid):  # noqa: E501
    """Retrieve a test artifact

     # noqa: E501

    :param testartifact_uuid: UUID of the test artifact to return
    :type testartifact_uuid: str

    :rtype: TestArtifact
    """
    testartifact = TestArtifactImpl.get_testartifact_by_uuid(testartifact_uuid)
    return testartifact_schema.dump(testartifact)


def get_testartifacts():  # noqa: E501
    """Get all test artifacts

     # noqa: E501


    :rtype: List[TestArtifact]
    """
    testartifacts = TestArtifactImpl.get_testartifacts()
    return testartifact_schema_many.dump(testartifacts)