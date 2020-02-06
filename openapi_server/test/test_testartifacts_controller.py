# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.post_testartifacts import POSTTestartifacts  # noqa: E501
from openapi_server.models.testartifact import Testartifact  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTestartifactsController(BaseTestCase):
    """TestartifactsController integration test stubs"""

    def test_create_testartifact(self):
        """Test case for create_testartifact

        Creates a testartifact
        """
        post_testartifacts = {
  "projectId" : 1
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/testartifacts',
            method='POST',
            headers=headers,
            data=json.dumps(post_testartifacts),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_testartifact_by_id(self):
        """Test case for download_testartifact_by_id

        Downloads the generated testartifact
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/testartifact/{testartifact_id}/download'.format(testartifact_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_testartifact_by_id(self):
        """Test case for get_testartifact_by_id

        Retrieve a testartifact
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/testartifact/{testartifact_id}'.format(testartifact_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_testartifacts(self):
        """Test case for get_testartifacts

        Get all testartifacts
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/testartifacts',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
