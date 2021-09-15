import base64

import git

from flask import current_app
from os import getenv, makedirs, path
from shutil import copytree, rmtree
from sqlalchemy import Boolean, Column, String
from urllib.parse import urlparse
import json
import ast
import urllib.parse
import yaml

from models.deployment import Deployment
from models.execution import Execution
from models.project import Project
from models.result import Result
from models.testartifact import TestArtifact

MANDATORY_FIELDS = ['name', 'repository_url', 'sut_tosca_path', 'ti_tosca_path', 'result_destination_path', 'test_id']


class Workflow:
    def __init__(self, workflow_yaml):
        self.__workflow_runs = []
        self.__outputs: {} = {}
        if 'name' in workflow_yaml:
            self.__workflow_runs.append(workflow_yaml)
        else:
            for entry in workflow_yaml:
                self.__workflow_runs.append(entry)

    @property
    def workflow_outputs(self):
        return self.__outputs

    @classmethod
    def create(cls, workflow_data):
        payload = Workflow.decode_input(workflow_data)
        workflow: Workflow = Workflow(yaml.safe_load(payload))
        wf_results: {} = {}
        try:
            wf_results = workflow.run_workflows()
        finally:
            return_value: {} = {'logs': workflow.workflow_outputs, 'results': wf_results}
            return return_value

    @classmethod
    def decode_input(cls, input_to_decode: str) -> str:
        unquoted_input = urllib.parse.unquote(input_to_decode, 'utf-8')
        unquoted_plus_input = urllib.parse.unquote_plus(unquoted_input)
        return unquoted_plus_input.replace('workflow_data=', '', 1)

    def check_config(self, config, name):
        for field in MANDATORY_FIELDS:
            found: bool = False
            for entry in config:
                if field == entry:
                    found = True
                    break
            if not found:
                self.__outputs[name] = f'''Mandatory field {field} is not set in configuration file.'''
                return False
        return True

    def run_workflows(self):
        result_ids: {} = {}
        for config in self.__workflow_runs:
            test_id = config['test_id']
            result_ids[test_id] = None
            if self.check_config(config, test_id):
                print(f'Running workflow with {config}.')
                project_uuid = self.create_project(test_id, config['name'], config['repository_url'])
                if 'sut_inputs_path' not in config:
                    config['sut_inputs_path'] = None
                if 'ti_inputs_path' not in config:
                    config['ti_inputs_path'] = None
                testartifact_uuid = self.create_testartifact(test_id, project_uuid,
                                                             sut_tosca=config['sut_tosca_path'],
                                                             sut_inputs=config['sut_inputs_path'],
                                                             ti_tosca=config['ti_tosca_path'],
                                                             ti_inputs=config['ti_inputs_path'])
                deployment_uuid = self.create_deployment(test_id, testartifact_uuid)
                execution_uuid = self.create_execution(test_id, deployment_uuid)
                result_uuid = self.create_result(test_id, execution_uuid)
                result_ids[test_id] = result_uuid
            else:
                self.__outputs[test_id] += f'\nCheck config failed. Skipping.'

        return result_ids

    def create_project(self, test_id, project_name: str, project_repository_url: str):
        project = Project.create(project_name, project_repository_url)
        if project.uuid:
            self.__outputs[test_id] = f'\nCreated project: {project}'
            return project.uuid
        return None

    def create_testartifact(self, test_id, project_uuid, sut_tosca, ti_tosca, sut_inputs='', ti_inputs=''):
        if not project_uuid:
            self.__outputs[test_id] += f'\nNo Project UUID provided.'
        testartifact = TestArtifact.create(project_uuid, sut_tosca, sut_inputs, ti_tosca, ti_inputs)
        if len(testartifact) > 0 and testartifact[0].uuid:
            self.__outputs[test_id] += f'\nCreated testartifact: {testartifact[0]}'
            return testartifact[0].uuid
        return None

    def create_deployment(self, test_id, testartifact_uuid):
        if not testartifact_uuid:
            self.__outputs[test_id] += f'\nNo Testartifact UUID provided.'
        deployment = Deployment.create(testartifact_uuid)
        if deployment.uuid:
            self.__outputs[test_id] += f'\nCreated deployment: {deployment}'
            return deployment.uuid
        return None

    def create_execution(self, test_id, deployment_uuid):
        if not deployment_uuid:
            self.__outputs[test_id] += f'\nNo Deployment UUID provided.'
        execution = Execution.create(deployment_uuid)
        if execution.uuid:
            self.__outputs[test_id] += f'\nCreated execution: {execution}'
            return execution.uuid
        return None

    def create_result(self, test_id, execution_uuid):
        if not execution_uuid:
            self.__outputs[test_id] += f'\nNo Execution UUID provided.'
        result = Result.create(execution_uuid)
        if result.uuid:
            self.__outputs[test_id] += f'\nCreated result: {result}'
            return result.uuid
        return None
