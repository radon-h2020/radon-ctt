# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.execution import Execution  # noqa: E501
from openapi_server.models.post_execution import POSTExecution  # noqa: E501
from openapi_server.test import BaseTestCase


class TestExecutionController(BaseTestCase):
    """ExecutionController integration test stubs"""

    def test_create_execution(self):
        """Test case for create_execution

        Creates an execution
        """
        post_execution = {
  "project_uuid" : "ac9431bd-1a1c-4d6f-a98f-cc97401b5e47",
  "testartifact_uuid" : "0036bd60-1ac0-44db-9578-0181792e2ac1",
  "deployment_uuid" : "1f89586a-8fd8-4766-baed-28b615809b14"
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/execution',
            method='POST',
            headers=headers,
            data=json.dumps(post_execution),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_execution_by_uuid(self):
        """Test case for get_execution_by_uuid

        Retrieve an execution
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/execution/{execution_uuid}'.format(execution_uuid='execution_uuid_example'),
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
