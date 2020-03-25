# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.post_test_artifact import POSTTestArtifact  # noqa: E501
from openapi_server.models.test_artifact import TestArtifact  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTestArtifactController(BaseTestCase):
    """TestArtifactController integration test stubs"""

    def test_create_testartifact(self):
        """Test case for create_testartifact

        Creates a test artifact
        """
        post_test_artifact = {
  "project_uuid" : "ac9431bd-1a1c-4d6f-a98f-cc97401b5e47",
  "sut_tosca_path" : "radon-ctt/sut_tosca.yml",
  "ti_tosca_path" : "radon-ctt/ti_tosca.yml"
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/testartifact',
            method='POST',
            headers=headers,
            data=json.dumps(post_test_artifact),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_testartifact_by_uuid(self):
        """Test case for download_testartifact_by_uuid

        Downloads the generated test artifact
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/testartifact/{testartifact_uuid}/download'.format(testartifact_uuid='testartifact_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_testartifact_by_uuid(self):
        """Test case for get_testartifact_by_uuid

        Retrieve a test artifact
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/testartifact/{testartifact_uuid}'.format(testartifact_uuid='testartifact_uuid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_testartifacts(self):
        """Test case for get_testartifacts

        Get all test artifacts
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/testartifact',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
