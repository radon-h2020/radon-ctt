import connexion
import os
import six

from flask import Response, send_file

from openapi_server.models.result import Result  # noqa: E501
from openapi_server import util

from models.result import Result as ResultImpl
from util.marhsmallow_schemas import ResultSchema

result_schema = ResultSchema()
result_schema_many = ResultSchema(many=True)


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
    return_file = os.path.join(result.fq_storage_path, result.results_file)
    if os.path.isfile(return_file):
        return send_file(return_file, as_attachment=True, attachment_filename="Results.zip")
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
