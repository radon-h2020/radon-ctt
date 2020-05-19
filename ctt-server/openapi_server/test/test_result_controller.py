# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.result import Result  # noqa: E501
from openapi_server.test import BaseTestCase


class TestResultController(BaseTestCase):
    """ResultController integration test stubs"""

    def test_create_result(self):
        """Test case for create_result

        Creates new result
        """
        body = POSTResult()
        response = self.client.open(
            '/result',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_result_by_uuid(self):
        """Test case for delete_result_by_uuid

        Delete a result
        """
        response = self.client.open(
            '/result/{result_uuid}'.format(result_uuid='result_uuid_example'),
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
        response = self.client.open(
            '/RadonCTT/result/{result_uuid}/download'.format(result_uuid='result_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_result_by_uuid(self):
        """Test case for get_result_by_uuid

        Retrieve a result
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/result/{result_uuid}'.format(result_uuid='result_uuid_example'),
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
