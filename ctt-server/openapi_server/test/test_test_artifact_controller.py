# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.post_test_artifact import POSTTestArtifact  # noqa: E501
from openapi_server.models.test_artifact import TestArtifact  # noqa: E501
from openapi_server.test import BaseTestCase

from test_util import TestUtil


class TestTestArtifactController(BaseTestCase):
    """TestArtifactController integration test stubs"""

    def setUp(self) -> None:
        response = TestUtil.create('project', self.client)
        self.project_uuid = json.loads(response.data.decode('utf-8'))['uuid']

        response = TestUtil.create('testartifact', self.client, self.project_uuid)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertGreater(len(response_json), 0)
        self.assertIn('uuid', response_json[0])
        self.testartifact_uuid = response_json[0]['uuid']
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def tearDown(self) -> None:
        TestUtil.delete('testartifact', self.client)
        TestUtil.delete('project', self.client)

    def test_create_testartifact(self):
        """Test case for create_testartifact

        Creates a test artifact
        """

        response = TestUtil.create('testartifact', self.client, self.project_uuid)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip  # no reason needed
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

    def test_delete_testartifact(self):
        """Test case for delete_project

        Delete a project
        """
        headers = {}
        response = self.client.open(
            '/RadonCTT/testartifact/{testartifact_uuid}'.format(testartifact_uuid=self.testartifact_uuid),
            method='DELETE',
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
            '/RadonCTT/testartifact/{testartifact_uuid}'.format(testartifact_uuid=self.testartifact_uuid),
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
