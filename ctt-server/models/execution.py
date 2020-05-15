import os
import requests
import uuid

from flask import current_app
from sqlalchemy import Column, String, ForeignKey

from db_orm.database import Base, db_session
from models.abstract_model import AbstractModel
from models.deployment import Deployment
from util.configuration import BasePath


class Execution(Base, AbstractModel):
    __tablename__ = 'execution'

    uuid: str
    deployment_uuid: str
    agent_configuration_uuid: str
    agent_execution_uuid: str

    uuid = Column(String, primary_key=True)
    deployment_uuid = Column(String, ForeignKey('deployment.uuid'), nullable=False)
    agent_configuration_uuid = Column(String)
    agent_execution_uuid = Column(String)

    config_uuid = None

    def __init__(self, deployment):
        self.uuid = str(uuid.uuid4())
        self.deployment_uuid = deployment.uuid
        self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)
        self.agent_configuration_uuid = None
        self.agent_execution_uuid = None

        if deployment:
            db_session.add(self)
            db_session.commit()
        else:
            raise Exception(f'Linked entities do not exist.')

    def __repr__(self):
        return '<Execution UUID=%r, AGENT_CONFIG_UUID=%r, AGENT_EXEC_UUID=%r>' % \
               (self.uuid, self.agent_configuration_uuid, self.agent_execution_uuid)

    def configure(self):
        # Check if running in Docker
        import subprocess
        host_address = 'localhost'
        if os.path.isfile('/.dockerenv'):
            # Running in docker
            host_address = subprocess.getoutput("ip route show 0/0 | awk '{print $3}'")
        else:
            # Running natively
            host_address = subprocess.getoutput('docker network inspect docker-compose_default | grep "docker-compose_edge-router_1" -A 3 | grep "IPv4Address" | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}"')
            # subprocess.getoutput("ip route show | grep 'docker' | awk '{print $9}'")

        current_app.logger.info(f'Determined {host_address} as docker host IP address.')
        data = {'host': host_address, 'port': '80'}
        files = {'test_plan': open('/tmp/testplan.jmx', 'rb')}
        response = requests.post('http://localhost:5000/jmeter/configuration', data=data, files=files)
        json_response = response.json()
        config_uuid = None
        if 'configuration' in json_response and 'uuid' in json_response['configuration']:
            config_uuid = json_response['configuration']['uuid']
            current_app.logger.info(f'Configuration has ID {config_uuid}.')
            self.agent_configuration_uuid = config_uuid
            db_session.commit()
        return config_uuid

    def execute(self, config_uuid):
        execution_uuid = None
        if config_uuid:
            data = {'config_uuid':config_uuid}
            response = requests.post('http://localhost:5000/jmeter/loadtest', data=data)
            json_response = response.json()
            if 'uuid' in json_response:
                execution_uuid = json_response['uuid']
                current_app.logger.info(f'Execution has ID {execution_uuid}.')
                self.agent_execution_uuid = execution_uuid
                db_session.commit()
        return execution_uuid

    @classmethod
    def get_parent_type(cls):
        return Deployment

    @classmethod
    def create(cls, deployment_uuid):
        linked_deployment = Deployment.get_by_uuid(deployment_uuid)
        execution = Execution(linked_deployment)
        config_uuid = execution.configure()
        if config_uuid:
            exec_uuid = execution.execute(config_uuid)
        else:
            current_app.logger.info("Execution could not be triggered. No config_uuid provided.")
        return execution

    @classmethod
    def get_all(cls):
        return Execution.query.all()

    @classmethod
    def get_by_uuid(cls, get_uuid):
        return Execution.query.filter_by(uuid=get_uuid).first()

    @classmethod
    def delete_by_uuid(cls, del_uuid):
        execution = Execution.query.filter_by(uuid=del_uuid)
        if execution:
            from models.result import Result
            linked_results = Result.query.filter_by(execution_uuid=del_uuid)
            for result in linked_results:
                Result.delete_by_uuid(result.uuid)
            execution.delete()
            # rmtree(self.fq_storage_path)
            db_session.commit()
