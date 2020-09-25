# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class POSTTestArtifact(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, project_uuid=None, sut_tosca_path=None, ti_tosca_path=None, inputs_file=None):  # noqa: E501
        """POSTTestArtifact - a model defined in OpenAPI

        :param project_uuid: The project_uuid of this POSTTestArtifact.  # noqa: E501
        :type project_uuid: str
        :param sut_tosca_path: The sut_tosca_path of this POSTTestArtifact.  # noqa: E501
        :type sut_tosca_path: str
        :param ti_tosca_path: The ti_tosca_path of this POSTTestArtifact.  # noqa: E501
        :type ti_tosca_path: str
        """
        self.openapi_types = {
            'project_uuid': str,
            'sut_tosca_path': str,
            'ti_tosca_path': str,
            'inputs_file': str
        }

        self.attribute_map = {
            'project_uuid': 'project_uuid',
            'sut_tosca_path': 'sut_tosca_path',
            'ti_tosca_path': 'ti_tosca_path',
            'inputs_file': 'inputs_file'
        }

        self._project_uuid = project_uuid
        self._sut_tosca_path = sut_tosca_path
        self._ti_tosca_path = ti_tosca_path
        self._inputs_file = inputs_file

    @classmethod
    def from_dict(cls, dikt) -> 'POSTTestArtifact':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The POSTTestArtifact of this POSTTestArtifact.  # noqa: E501
        :rtype: POSTTestArtifact
        """
        return util.deserialize_model(dikt, cls)

    @property
    def project_uuid(self):
        """Gets the project_uuid of this POSTTestArtifact.


        :return: The project_uuid of this POSTTestArtifact.
        :rtype: str
        """
        return self._project_uuid

    @project_uuid.setter
    def project_uuid(self, project_uuid):
        """Sets the project_uuid of this POSTTestArtifact.


        :param project_uuid: The project_uuid of this POSTTestArtifact.
        :type project_uuid: str
        """
        if project_uuid is None:
            raise ValueError("Invalid value for `project_uuid`, must not be `None`")  # noqa: E501

        self._project_uuid = project_uuid

    @property
    def sut_tosca_path(self):
        """Gets the sut_tosca_path of this POSTTestArtifact.


        :return: The sut_tosca_path of this POSTTestArtifact.
        :rtype: str
        """
        return self._sut_tosca_path

    @sut_tosca_path.setter
    def sut_tosca_path(self, sut_tosca_path):
        """Sets the sut_tosca_path of this POSTTestArtifact.


        :param sut_tosca_path: The sut_tosca_path of this POSTTestArtifact.
        :type sut_tosca_path: str
        """
        if sut_tosca_path is None:
            raise ValueError("Invalid value for `sut_tosca_path`, must not be `None`")  # noqa: E501

        self._sut_tosca_path = sut_tosca_path

    @property
    def ti_tosca_path(self):
        """Gets the ti_tosca_path of this POSTTestArtifact.


        :return: The ti_tosca_path of this POSTTestArtifact.
        :rtype: str
        """
        return self._ti_tosca_path

    @ti_tosca_path.setter
    def ti_tosca_path(self, ti_tosca_path):
        """Sets the ti_tosca_path of this POSTTestArtifact.


        :param ti_tosca_path: The ti_tosca_path of this POSTTestArtifact.
        :type ti_tosca_path: str
        """
        if ti_tosca_path is None:
            raise ValueError("Invalid value for `ti_tosca_path`, must not be `None`")  # noqa: E501

        self._ti_tosca_path = ti_tosca_path

    @property
    def inputs_file(self):
        """Gets the input_file of this POSTTestArtifact.


        :return: The input_file of this POSTTestArtifact.
        :rtype: str
        """
        return self._inputs_file

    @inputs_file.setter
    def inputs_file(self, inputs_file):
        """Sets the ti_tosca_path of this POSTTestArtifact.


        :param ti_tosca_path: The ti_tosca_path of this POSTTestArtifact.
        :type ti_tosca_path: str
        """
        if inputs_file is None:
            raise ValueError("Invalid value for `input_file`, must not be `None`")  # noqa: E501

        self._inputs_file = inputs_file
