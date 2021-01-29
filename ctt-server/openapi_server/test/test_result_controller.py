# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.result import Result  # noqa: E501
from openapi_server.test import BaseTestCase

from test_util import TestUtil


class TestResultController(BaseTestCase):
    """ResultController integration test stubs"""

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

        response = TestUtil.create('result', self.client, self.execution_uuid)
        response_json = json.loads(response.data.decode('utf-8'))
        self.result_uuid = response_json['uuid']
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def tearDown(self) -> None:
        TestUtil.delete('result', self.client)
        TestUtil.delete('execution', self.client)
        TestUtil.delete('deployment', self.client)
        TestUtil.delete('testartifact', self.client)
        TestUtil.delete('project', self.client)

    def test_create_result(self):
        """Test case for create_result

        Creates new result
        """
        response = TestUtil.create('result', self.client, self.execution_uuid)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_result_by_uuid(self):
        """Test case for delete_result_by_uuid

        Delete a result
        """
        response = self.client.open(
            '/RadonCTT/result/{result_uuid}'.format(result_uuid=self.result_uuid),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_result_by_uuid(self):
        """Test case for download_result_by_uuid

        Downloads the generated results
        """
        headers = { 
            'Accept': 'application/json',
        }

        with self.client.open(
            '/RadonCTT/result/{result_uuid}/download'.format(result_uuid=self.result_uuid),
            method='GET',
            headers=headers) as response:
            self.assert200(response)

    def test_get_result_by_uuid(self):
        """Test case for get_result_by_uuid

        Retrieve a result
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/result/{result_uuid}'.format(result_uuid=self.result_uuid),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_results(self):
        """Test case for get_results

        Get all results
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/result',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
