# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.execution import Execution  # noqa: E501
from openapi_server.models.post_execution import POSTExecution  # noqa: E501
from openapi_server.test import BaseTestCase

from test_util import TestUtil


class TestExecutionController(BaseTestCase):
    """ExecutionController integration test stubs"""

    def setUp(self) -> None:
        response = TestUtil.create('project', self.client)
        self.project_uuid = json.loads(response.data.decode('utf-8'))['uuid']

        response = TestUtil.create('testartifact', self.client, self.project_uuid)
        response_json = json.loads(response.data.decode('utf-8'))
        self.testartifact_uuid = response_json[0]['uuid']

        response = TestUtil.create('deployment', self.client, self.testartifact_uuid)
        response_json = json.loads(response.data.decode('utf-8'))
        self.deployment_uuid = response_json['uuid']

        response = TestUtil.create('execution', self.client, self.deployment_uuid)
        response_json = json.loads(response.data.decode('utf-8'))
        self.execution_uuid = response_json['uuid']
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def tearDown(self) -> None:
        TestUtil.delete('execution', self.client)
        TestUtil.delete('deployment', self.client)
        TestUtil.delete('testartifact', self.client)
        TestUtil.delete('project', self.client)

    def test_create_execution(self):
        """Test case for create_execution

        Creates an execution
        """
        response = TestUtil.create('execution', self.client, self.deployment_uuid)
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_get_execution_by_uuid(self):
        """Test case for get_execution_by_uuid

        Retrieve an execution
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/execution/{execution_uuid}'.format(execution_uuid=self.execution_uuid),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_executions(self):
        """Test case for get_executions

        Get all executions
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/execution',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
