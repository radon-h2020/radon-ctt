# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.executor import Executor  # noqa: E501
from openapi_server.models.post_executors import POSTExecutors  # noqa: E501
from openapi_server.test import BaseTestCase


class TestExecutorsController(BaseTestCase):
    """ExecutorsController integration test stubs"""

    def test_create_executor(self):
        """Test case for create_executor

        Creates an executor
        """
        post_executors = {
  "deploymentId" : 1
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/executors',
            method='POST',
            headers=headers,
            data=json.dumps(post_executors),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_executor_by_id(self):
        """Test case for get_executor_by_id

        Retrieve a executor
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/executor/{executor_id}'.format(executor_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_executors(self):
        """Test case for get_executors

        Get all executors
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/executors',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
