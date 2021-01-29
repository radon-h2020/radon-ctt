# coding: utf-8

import json
from flask_testing.utils import TestCase


class TestUtil:
    post = {
        'project': {
            "name": "TestProject",
            "repository_url": "https://github.com/radon-h2020/demo-ctt-todolistapi.git"
        },
        'testartifact': {
            "sut_tosca_path": "todolist.csar",
            "ti_tosca_path": "deploymentTestAgent.csar",
            "ti_inputs_path": "inputs.yaml"
        },
        'deployment': {},
        'execution': {},
        'result': {},
    }

    resources = ['project', 'testartifact', 'deployment', 'execution', 'result']

    @classmethod
    def create(cls, target_resource: str, client: TestCase, uuid: str = None):
        post_data = TestUtil.post[target_resource]
        resource_index = TestUtil.resources.index(target_resource)
        if resource_index > 0:
            post_data[f'{TestUtil.resources[resource_index-1]}_uuid'] = uuid
        headers = {'Content-Type': 'application/json'}
        response = client.open(
            f'/RadonCTT/{target_resource}',
            method='POST',
            headers=headers,
            data=json.dumps(post_data),
            content_type='application/json')
        return response

    @classmethod
    def delete(cls, target_resource: str, client: TestCase):
        headers = {
            'Accept': 'application/json',
        }
        response = client.open(
            f'/RadonCTT/{target_resource}',
            method='GET',
            headers=headers)

        items = json.loads(response.data.decode('utf-8'))
        for item in items:
            api_url = '/RadonCTT/{resource}/{uuid}'.format(resource=target_resource, uuid=item['uuid'])
            client.open(
                api_url,
                method='DELETE',
                headers={})

