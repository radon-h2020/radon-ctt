import connexion
import six

from openapi_server.models.result import Result  # noqa: E501
from openapi_server import util

# from models.result import Result as ResultImpl
from util.marhsmallow_schemas import ResultSchema

result_schema = ResultSchema()
result_schema_many = ResultSchema(many=True)


def download_result_by_uuid(result_uuid):  # noqa: E501
    """Downloads the generated results

     # noqa: E501

    :param result_uuid: UUID of the result to download
    :type result_uuid: str

    :rtype: file
    """
    raise Exception('Not Implemented')
    return 'do some magic!'


def get_result_by_uuid(result_uuid):  # noqa: E501
    """Retrieve a result

     # noqa: E501

    :param result_uuid: UUID of the result to return
    :type result_uuid: str

    :rtype: Result
    """
    result = ResultImpl.get_result_by_uuid(result_uuid)
    return result_schema.dump(result)


def get_results():  # noqa: E501
    """Get all results

     # noqa: E501


    :rtype: List[Result]
    """
    results = ResultImpl.get_results()
    return result_schema_many.dump(results)