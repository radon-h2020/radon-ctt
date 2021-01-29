# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.deployment import Deployment  # noqa: E501
from openapi_server.models.post_deployment import POSTDeployment  # noqa: E501
from openapi_server.test import BaseTestCase

from test_util import TestUtil


class TestDeploymentController(BaseTestCase):
    """DeploymentController integration test stubs"""

    def setUp(self) -> None:
        response = TestUtil.create('project', self.client)
        self.project_uuid = json.loads(response.data.decode('utf-8'))['uuid']

        response = TestUtil.create('testartifact', self.client, self.project_uuid)
        response_json = json.loads(response.data.decode('utf-8'))
        self.testartifact_uuid = response_json[0]['uuid']

        response = TestUtil.create('deployment', self.client, self.testartifact_uuid)
        response_json = json.loads(response.data.decode('utf-8'))
        self.deployment_uuid = response_json['uuid']
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def tearDown(self) -> None:
        TestUtil.delete('deployment', self.client)
        TestUtil.delete('testartifact', self.client)
        TestUtil.delete('project', self.client)

    def test_create_deployment(self):
        """Test case for create_deployment

        Creates a deployment
        """
        response = TestUtil.create('deployment', self.client, self.testartifact_uuid)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_deployment_by_uuid(self):
        """Test case for get_deployment_by_uuid

        Retrieve a deployment
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/deployment/{deployment_uuid}'.format(deployment_uuid=self.deployment_uuid),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_deployments(self):
        """Test case for get_deployments

        Get all deployments
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/deployment',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
