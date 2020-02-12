# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.deployment import Deployment  # noqa: E501
from openapi_server.models.post_deployments import POSTDeployments  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDeploymentsController(BaseTestCase):
    """DeploymentsController integration test stubs"""

    def test_create_deployment(self):
        """Test case for create_deployment

        Creates a deployment
        """
        post_deployments = {
  "testartifactId" : 1
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/deployments',
            method='POST',
            headers=headers,
            data=json.dumps(post_deployments),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_deployment_by_id(self):
        """Test case for get_deployment_by_id

        Retrieve a deployment
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/deployment/{deployment_id}'.format(deployment_id=56),
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
            '/RadonCTT/deployments',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
