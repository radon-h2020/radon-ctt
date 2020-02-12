# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.post_projects import POSTProjects  # noqa: E501
from openapi_server.models.project import Project  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProjectsController(BaseTestCase):
    """ProjectsController integration test stubs"""

    def test_create_project(self):
        """Test case for create_project

        Creates a project
        """
        post_projects = {
  "servicetemplate_location" : "radon-ctt/servicetemplate.yml",
  "file" : "",
  "repository_url" : "https://github.com/UST-CTT/radon-ctt-sockshop-example.git"
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/projects',
            method='POST',
            headers=headers,
            data=json.dumps(post_projects),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_project(self):
        """Test case for delete_project

        Delete a project
        """
        headers = { 
        }
        response = self.client.open(
            '/RadonCTT/project/{project_id}'.format(project_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_project_by_id(self):
        """Test case for get_project_by_id

        Retrieve a project
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/project/{project_id}'.format(project_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_projects(self):
        """Test case for get_projects

        Get a list of projects
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/RadonCTT/projects',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
