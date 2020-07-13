import os
import requests
import shutil
import tempfile

from flask import current_app

name = 'JMeter'
plugin_name = 'jmeter'
plugin_type = 'radon.policies.testing.JMeterLoadTest'

"""
'SimpleJMeterLoadTest': {
    'type': 'radon.policies.testing.JMeterLoadTest',
    'properties': {
        'jmx_file': 'sockshop.jmx',
        'hostname': 'localhost',
        'port': 8080,
        'ti_blueprint': 'radon.blueprints.testing.JMeterMasterOnly',
        'user.properties': None,
        'test_id': 'loadtest213',
    },
    'targets': ['SockShop'],
}
"""


def configure(ti_hostname, policy_yaml, test_artifact_storage_path, sut_hostname=None, ti_port=5000):

    policy_properties = policy_yaml['properties']

    # TODO: Move JMeter-specific properties and their handling/parsing to separate class?
    jmx_file = ''
    if 'jmx_file' in policy_properties:
        jmx_file = os.path.join(test_artifact_storage_path, 'radon-ctt', policy_properties['jmx_file'])

    if not sut_hostname and 'hostname' in policy_properties:
        sut_hostname = policy_properties['hostname']

    sut_port = None
    if 'port' in policy_properties:
        sut_port = policy_properties['port']

    user_properties = ''
    if 'user.properties' in policy_properties and not policy_properties['user.properties'] is None:
        user_properties = os.path.join(test_artifact_storage_path, 'radon-ctt', policy_properties['user.properties'])

    test_id = None
    if 'test_id' in policy_properties:
        test_id = policy_properties['test_id']

    if sut_hostname and sut_port and os.path.isfile(jmx_file) and test_id:
        data = {'host': sut_hostname, 'port': sut_port}
        files = {'test_plan': open(jmx_file, 'rb')}
        if os.path.isfile(user_properties):
            files['properties'] = open(user_properties, 'rb')

        response = requests.post(f'http://{ti_hostname}:{ti_port}/{plugin_name}/configuration', data=data, files=files)
        json_response = response.json()
        config_uuid = None
        if 'configuration' in json_response and 'uuid' in json_response['configuration']:
            config_uuid = json_response['configuration']['uuid']
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
