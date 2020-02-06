# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Deployment(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, project_id=None, status=None, testartifact_id=None):  # noqa: E501
        """Deployment - a model defined in OpenAPI

        :param id: The id of this Deployment.  # noqa: E501
        :type id: int
        :param project_id: The project_id of this Deployment.  # noqa: E501
        :type project_id: int
        :param status: The status of this Deployment.  # noqa: E501
        :type status: str
        :param testartifact_id: The testartifact_id of this Deployment.  # noqa: E501
        :type testartifact_id: int
        """
        self.openapi_types = {
            'id': int,
            'project_id': int,
            'status': str,
            'testartifact_id': int
        }

        self.attribute_map = {
            'id': 'id',
            'project_id': 'projectId',
            'status': 'status',
            'testartifact_id': 'testartifactId'
        }

        self._id = id
        self._project_id = project_id
        self._status = status
        self._testartifact_id = testartifact_id

    @classmethod
    def from_dict(cls, dikt) -> 'Deployment':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Deployment of this Deployment.  # noqa: E501
        :rtype: Deployment
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Deployment.


        :return: The id of this Deployment.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Deployment.


        :param id: The id of this Deployment.
        :type id: int
        """

        self._id = id

    @property
    def project_id(self):
        """Gets the project_id of this Deployment.


        :return: The project_id of this Deployment.
        :rtype: int
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this Deployment.


        :param project_id: The project_id of this Deployment.
        :type project_id: int
        """

        self._project_id = project_id

    @property
    def status(self):
        """Gets the status of this Deployment.


        :return: The status of this Deployment.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Deployment.


        :param status: The status of this Deployment.
        :type status: str
        """

        self._status = status

    @property
    def testartifact_id(self):
        """Gets the testartifact_id of this Deployment.


        :return: The testartifact_id of this Deployment.
        :rtype: int
        """
        return self._testartifact_id

    @testartifact_id.setter
    def testartifact_id(self, testartifact_id):
        """Sets the testartifact_id of this Deployment.


        :param testartifact_id: The testartifact_id of this Deployment.
        :type testartifact_id: int
        """

        self._testartifact_id = testartifact_id
