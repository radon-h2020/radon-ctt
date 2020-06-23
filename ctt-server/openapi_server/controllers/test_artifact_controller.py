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
        post_test_artifact = POSTTestArtifact.from_dict(connexion.request.get_json())  # noqa: E501
    created_testartifacts = TestArtifactImpl.create(
        post_test_artifact.project_uuid, post_test_artifact.sut_tosca_path, post_test_artifact.ti_tosca_path)
    return testartifact_schema_many.dump(created_testartifacts)


def delete_testartifact_by_uuid(testartifact_uuid):  # noqa: E501
    """Delete a test artifact

    Deletes the test artifact with the given UUID and all elements depending on it # noqa: E501

    :param testartifact_uuid: UUID of the test artifact to delete
    :type testartifact_uuid: str

    :rtype: TestArtifact
    """
    deleted_testartifact = TestArtifactImpl.delete_by_uuid(testartifact_uuid)
    return testartifact_schema.dump(deleted_testartifact)


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
    testartifact = TestArtifactImpl.get_by_uuid(testartifact_uuid)
    return testartifact_schema.dump(testartifact)


def get_testartifacts():  # noqa: E501
    """Get all test artifacts

     # noqa: E501


    :rtype: List[TestArtifact]
    """
    testartifacts = TestArtifactImpl.get_all()
    return testartifact_schema_many.dump(testartifacts)
