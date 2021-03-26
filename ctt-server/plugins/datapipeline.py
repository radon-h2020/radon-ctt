import os
import requests
import shutil
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

from flask import current_app

name = 'DataPipeline'
plugin_name = 'datapipeline'
plugin_type = 'radon.policies.testing.DataPipelineLoadTest'

"""
    - DataPipelineLoadTest:
        type: radon.policies.testing.DataPipelineLoadTest
        properties:
          velocity_per_minute: "60"
          hostname: "radon.s3.eu-central-1.amazonaws.com"
          port: "8080"
          ti_blueprint: "radon.blueprints.testing.NiFiTIDocker"
          resource_location: "/tmp/resources.zip"
          test_duration_sec: "60"
          test_id: "firstdptest"
        targets: [ ConsS3Bucket_1 ]
"""


def configure(ti_hostname, policy_yaml, test_artifact_storage_path, sut_hostname=None, ti_port=5000):

    policy_properties = policy_yaml['properties']


    #resource_location
    resource_location = ''
    if 'resource_location' in policy_properties:
        resources = os.path.join(test_artifact_storage_path, policy_properties['resource_location'])

    #hostname
    if not sut_hostname and 'hostname' in policy_properties:
        sut_hostname = policy_properties['hostname']

    # port
    # - not used
    sut_port = None
    if 'port' in policy_properties:
        sut_port = policy_properties['port']

    #velocity_per_minute
    velocity_per_minute = None
    if 'velocity_per_minute' in policy_properties:
        velocity_per_minute = policy_properties['velocity_per_minute']

    #test_duration_sec
    test_duration_sec = None
    if 'test_duration_sec' in policy_properties:
        test_duration_sec = policy_properties['test_duration_sec']


    # test_id
    test_id = None
    if 'test_id' in policy_properties:
        test_id = policy_properties['test_id']



    if sut_hostname and resources and test_duration_sec and velocity_per_minute and os.path.isfile(resources) and test_id:
        # Check if resources file is a zip file.
        if resources.endswith('.zip'):
            # No action needed, as a zip file is already provided by the user.
            current_app.logger.debug(f'ZIP file {resources} was provided.')
            pass
        else:
            raise ValueError(f'{resources} is not of a valid file type. Needs to be .jmx or .zip.')

        data = {'host': sut_hostname, 'test_duration_sec': test_duration_sec, 'velocity_per_minute': velocity_per_minute}

        files = {'resources': open(resources, 'rb')}

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


