import connexion
import os
import six

from flask import Response, send_file

from openapi_server.models.post_result import POSTResult
from openapi_server.models.result import Result  # noqa: E501
from openapi_server import util

from models.result import Result as ResultImpl
from util.marhsmallow_schemas import ResultSchema

result_schema = ResultSchema()
result_schema_many = ResultSchema(many=True)

def create_result(post_result=None):  # noqa: E501
    """Creates a new result

     # noqa: E501

    :param post_result:
    :type post_result: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        post_result = POSTResult.from_dict(connexion.request.get_json())  # noqa: E501

    created_result = ResultImpl.create(post_result.execution_uuid)
    return result_schema.dump(created_result)


def delete_result_by_uuid(result_uuid):  # noqa: E501
    """Delete a result

    Deletes the result with the given UUID on it # noqa: E501

    :param result_uuid: UUID of the result to delete
    :type result_uuid: str

    :rtype: Result
    """
    result = ResultImpl.delete_by_uuid(result_uuid)
    return result_schema.dump(result)


def download_result_by_uuid(result_uuid):  # noqa: E501
    """Downloads the generated results

     # noqa: E501

    :param result_uuid: UUID of the result to download
    :type result_uuid: str

    :rtype: file
    """
    result = ResultImpl.get_by_uuid(result_uuid)
    if os.path.isfile(result.fq_result_storage_path):
        return send_file(result.fq_result_storage_path, as_attachment=True, attachment_filename="Results.zip")
    else:
        return None


def get_result_by_uuid(result_uuid):  # noqa: E501
    """Retrieve a result

     # noqa: E501

    :param result_uuid: UUID of the result to return
    :type result_uuid: str

    :rtype: Result
    """
    result = ResultImpl.get_by_uuid(result_uuid)
    return result_schema.dump(result)


def get_results():  # noqa: E501
    """Get all results

     # noqa: E501


    :rtype: List[Result]
    """
    results = ResultImpl.get_all()
    return result_schema_many.dump(results)
