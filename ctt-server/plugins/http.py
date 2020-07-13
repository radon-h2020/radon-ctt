import requests
import shutil
import tempfile

from flask import current_app

name = 'HTTP'
plugin_name = 'http'
plugin_type = 'radon.policies.testing.HttpEndpointTest'

"""
    SimpleEndpointTest:
      type: radon.policies.testing.HttpEndpointTest
      properties:
        path: "/cart/"
        hostname: "localhost"
        method: "GET"
        port: 80
        expected_status: 200
        expected_body: null
        ti_blueprint: null
        use_https: true
        test_body: null
        test_header: null
        test_id: null
      targets: [ SockShop ]
"""


def configure(ti_hostname, policy_yaml, test_artifact_storage_path, sut_hostname=None, ti_port=5000):

    policy_properties = policy_yaml['properties']

    # TODO: Move HTTP-specific properties and their handling/parsing to separate class?
    path = '/'
    if 'path' in policy_properties:
        path = policy_properties['path']

    if not sut_hostname and 'hostname' in policy_properties:
        sut_hostname = policy_properties['hostname']

    port = None
    if 'port' in policy_properties:
        port = policy_properties['port']

    method = None
    if 'method' in policy_properties:
        method = policy_properties['method']

    test_id = None
    if 'test_id' in policy_properties:
        test_id = policy_properties['test_id']

    expected_status = None
    if 'expected_status' in policy_properties:
        expected_status = policy_properties['expected_status']

    use_https = None
    if 'use_https' in policy_properties:
        use_https = policy_properties['use_https']

    test_body = None
    if 'test_body' in policy_properties:
        test_body = policy_properties['test_body']

    test_header = None
    if 'test_header' in policy_properties:
        test_header = policy_properties['test_header']

    if sut_hostname and port and method and path and expected_status and test_id:

        data = {'hostname': sut_hostname,
                'port': port,
                'method': method,
                'path': path,
                'expected_status': expected_status,
                'test_id': test_id, }

        if use_https:
            data['use_https'] = use_https

        if test_body:
            data['test_body'] = test_body

        if test_header:
            data['test_header'] = test_header

        response = requests.post(f'http://{ti_hostname}:{ti_port}/{plugin_name}/configuration', data=data)
        json_response = response.json()
        config_uuid = None
        if 'uuid' in json_response:
            config_uuid = json_response['uuid']
            current_app.logger.info(f'Configuration has ID {config_uuid}.')
        return config_uuid
    else:
        current_app.logger.error(f'Test information incomplete to finalize configuration.')
        raise ValueError(f'Test information incomplete to finalize configuration.')


def execute(ti_hostname, config_uuid, ti_port=5000):
    if config_uuid:
        data = {'config_uuid': config_uuid}
        response = requests.post(f'http://{ti_hostname}:{ti_port}/{plugin_name}/execution', data=data)
        json_response = response.json()
        if 'uuid' in json_response:
            execution_uuid = json_response['uuid']
            current_app.logger.info(f'Execution has ID {execution_uuid}.')
            return execution_uuid


def get_results(ti_hostname, execution_uuid, ti_port=5000):
    if execution_uuid:
        # Download results from test infrastructure
        with requests.get(
                f'http://{ti_hostname}:{ti_port}/{plugin_name}/execution/{execution_uuid}', stream=True) as req:
            temp_results = tempfile.NamedTemporaryFile(delete=False)
            with open(temp_results.name, 'wb') as f:
                shutil.copyfileobj(req.raw, f)
            return temp_results.name

