# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.deployment import Deployment  # noqa: E501
from openapi_server.models.post_deployment import POSTDeployment  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDeploymentController(BaseTestCase):
    """DeploymentController integration test stubs"""

    def test_create_deployment(self):
        """Test case for create_deployment

        Creates a deployment
        """
        post_deployment = {
  "project_uuid" : "ac9431bd-1a1c-4d6f-a98f-cc97401b5e47",
  "testartifact_uuid" : "0036bd60-1ac0-44db-9578-0181792e2ac1"
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/deployment',
            method='POST',
            headers=headers,
            data=json.dumps(post_deployment),
            content_type='application/json')
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
            '/RadonCTT/deployment/{deployment_uuid}'.format(deployment_uuid='deployment_uuid_example'),
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
