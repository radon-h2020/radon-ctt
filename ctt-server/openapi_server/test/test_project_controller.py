# coding: utf-8

from __future__ import absolute_import
import json
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.post_project import POSTProject  # noqa: E501
from openapi_server.models.project import Project  # noqa: E501
from openapi_server.test import BaseTestCase

from test_util import TestUtil


class TestProjectController(BaseTestCase):
    """ProjectController integration test stubs"""

    def setUp(self) -> None:
        response = TestUtil.create('project', self.client)
        self.project_uuid = json.loads(response.data.decode('utf-8'))['uuid']
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def tearDown(self) -> None:
        TestUtil.delete('project', self.client)

    def test_create_project(self):
        """Test case for create_project

        Creates a project
        """

        response = TestUtil.create('project', self.client)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_project(self):
        """Test case for delete_project

        Delete a project
        """
        headers = {}
        response = self.client.open(
            '/RadonCTT/project/{project_uuid}'.format(project_uuid=self.project_uuid),
            method='DELETE',
            headers=headers)
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

    def test_get_project_by_uuid(self):
        """Test case for get_project_by_uuid

        Retrieve a project
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/project/{project_uuid}'.format(project_uuid=self.project_uuid),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_projects(self):
        """Test case for get_projects

        Get a list of all projects
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/project',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIs(len(json.loads(response.data.decode('utf-8'))), 1, 'Exactly one project exists.')


if __name__ == '__main__':
    unittest.main()
