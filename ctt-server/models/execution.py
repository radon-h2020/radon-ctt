import os
import re
import requests
import subprocess
import uuid

from flask import current_app
from sqlalchemy import Column, String, ForeignKey

from db_orm.database import Base, db_session
from models.abstract_model import AbstractModel
from models.deployment import Deployment
from util.configuration import BasePath

ip_pattern = re.compile('([1][0-9][0-9].|^[2][5][0-5].|^[2][0-4][0-9].|^[1][0-9][0-9].|^[0-9][0-9].|^[0-9].)'
                        '([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)'
                        '([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)'
                        '([1][0-9][0-9]|[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[0-9][0-9]|[0-9])')


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
    sut_ip_address = Column(String)
    ti_ip_address = Column(String)

    def __init__(self, deployment):
        self.uuid = str(uuid.uuid4())
        self.deployment_uuid = deployment.uuid
        self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)

        if deployment:
            db_session.add(self)
            db_session.commit()
        else:
            raise Exception(f'Linked entities do not exist.')

    def __repr__(self):
        return '<Execution UUID=%r, AGENT_CONFIG_UUID=%r, AGENT_EXEC_UUID=%r>' % \
               (self.uuid, self.agent_configuration_uuid, self.agent_execution_uuid)

    @property
    def system_under_test_ip(self):
        return self.sut_ip_address

    @property
    def test_infrastructure_ip(self):
        return self.ti_ip_address

    @classmethod
    def deployment_workaround(cls):
        sut_ip = 'localhost'
        ti_ip = 'localhost'
        # if os.path.isfile('/.dockerenv'):
        #     # Running in docker
        #     host_address = subprocess.getoutput("ip route show 0/0 | awk '{print $3}'")
        #     sut_ip = host_address
        #     ti_ip = host_address
        # else:
        #     # Running natively
        docker_network = 'docker-compose_default'
        sut_docker_name = 'docker-compose_edge-router_1'

        if os.path.isfile('/.dockerenv'):
            subprocess.call(['docker', 'network', 'connect', docker_network, 'RadonCTT'])

        sut_ip = Execution.workaround_parse_ip(docker_network, sut_docker_name)

        ti_docker_name = 'JMeterAgent'
        subprocess.call(['docker', 'network', 'connect', docker_network, ti_docker_name])
        ti_ip = Execution.workaround_parse_ip(docker_network, ti_docker_name)

        current_app.logger.info(f'Determined SUT IP-address: {sut_ip}.')
        current_app.logger.info(f'Determined TI IP-address: {ti_ip}.')
        return {'sut': sut_ip, 'ti': ti_ip}

    @classmethod
    def workaround_parse_ip(cls, docker_network, docker_name):
        ip_address_line = subprocess.getoutput(
            f'docker network inspect {docker_network} | grep {docker_name} -A 3 | grep "IPv4Address"')
        ip_address = re.search(ip_pattern, ip_address_line).group()
        return ip_address

    def configure(self):
        ip_addresses = Execution.deployment_workaround()
        self.sut_ip_address = ip_addresses['sut']
        self.ti_ip_address = ip_addresses['ti']

        data = {'host': self.sut_ip_address, 'port': '80'}
        files = {'test_plan': open('/tmp/test_plan.jmx', 'rb')}
        response = requests.post(f'http://{self.ti_ip_address}:5000/jmeter/configuration', data=data, files=files)
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
            data = {'config_uuid': config_uuid}
            response = requests.post(f'http://{self.ti_ip_address}:5000/jmeter/loadtest', data=data)
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
