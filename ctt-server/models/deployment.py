import os
import re
import subprocess
import time
import uuid

from flask import current_app
from sqlalchemy import Column, String, ForeignKey

from db_orm.database import Base, db_session
from models.testartifact import TestArtifact
from models.abstract_model import AbstractModel
from util.configuration import BasePath, DropPolicies, FaasScenario
from util.tosca_helper import Csar

ip_pattern = re.compile('([1][0-9][0-9].|^[2][5][0-5].|^[2][0-4][0-9].|^[1][0-9][0-9].|^[0-9][0-9].|^[0-9].)'
                        '([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)'
                        '([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)'
                        '([1][0-9][0-9]|[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[0-9][0-9]|[0-9])')


class Deployment(Base, AbstractModel):
    __tablename__ = 'deployment'

    uuid: str
    testartifact_uuid: str
    storage_path: str
    status: str
    sut_hostname: str
    ti_hostname: str

    uuid = Column(String, primary_key=True)
    testartifact_uuid = Column(String, ForeignKey('testartifact.uuid'), nullable=False)
    sut_hostname = Column(String)
    ti_hostname = Column(String)

    def __init__(self, testartifact):
        self.uuid = str(uuid.uuid4())
        self.testartifact_uuid = testartifact.uuid
        self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)
        self.__test_artifact = testartifact
        self.sut_hostname = 'localhost'
        self.ti_hostname = 'localhost'

        if testartifact:
            db_session.add(self)
            db_session.commit()
        else:
            raise Exception(f'Linked entities do not exist.')

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def __repr__(self):
        return '<Deployment UUID=%r, TA_UUID=%r>' % (self.uuid, self.testartifact_uuid)

    @property
    def hostname_sut(self):
        return self.sut_hostname

    @property
    def hostname_ti(self):
        return self.ti_hostname

    def deploy(self):
        test_artifact = TestArtifact.get_by_uuid(self.testartifact_uuid)
        sut_csar_path = os.path.join(test_artifact.fq_storage_path, test_artifact.sut_tosca_path)
        ti_csar_path = os.path.join(test_artifact.fq_storage_path, test_artifact.ti_tosca_path)

        # Deployment of SuT
        with Csar(sut_csar_path, extract_dir=self.sut_storage_path, keep=True) as sut_csar:
            if DropPolicies:
                sut_csar.drop_policies()
            entry_definition = sut_csar.tosca_entry_point

            current_app.logger.\
                info(f'Deploying SuT {str(entry_definition)} with opera in folder {str(self.sut_storage_path)}.')
            subprocess.call(['opera', 'deploy', entry_definition], cwd=self.sut_storage_path)

        # Deployment of TI
        with Csar(ti_csar_path, extract_dir=self.ti_storage_path, keep=True) as ti_csar:
            if DropPolicies:
                ti_csar.drop_policies()
            entry_definition = ti_csar.tosca_entry_point

            if entry_definition:
                current_app.logger.\
                    info(f'Deploying TI {str(entry_definition)} with opera in folder {str(self.ti_storage_path)}.')
                subprocess.call(['opera', 'deploy', entry_definition], cwd=self.ti_storage_path)

        time.sleep(30)

        envFaasScenario = os.getenv('CTT_FAAS_ENABLED')
        faas_mode = False
        if envFaasScenario:
            if envFaasScenario == "1":
                faas_mode = True
        elif FaasScenario:
            faas_mode = True

        if faas_mode:
            # FaaS scenario
            deployed_systems = Deployment.deployment_workaround(exclude_sut=True)
            self.sut_hostname = self.__test_artifact.policy_yaml['properties']['hostname']
            self.ti_hostname = deployed_systems['ti']
        else:
            deployed_systems = Deployment.deployment_workaround(exclude_sut=False)
            self.sut_hostname = deployed_systems['sut']
            self.ti_hostname = deployed_systems['ti']

        db_session.add(self)
        db_session.commit()

    @classmethod
    def deployment_workaround(cls, exclude_sut):

        result_set = {}

        # Determine Docker network that is used on the current machine
        docker_network = subprocess.getoutput("docker network ls | grep compose | head -n1 | awk '{print $2}'")
        if docker_network:
            current_app.logger.info(f'Automatically determined docker network {docker_network}')
        else:
            docker_network = 'dockercompose_default'
            current_app.logger.info(
                f'Docker network could not be determined automatically. Falling back to {docker_network}')

        if os.path.isfile('/.dockerenv'):
            subprocess.call(['docker', 'network', 'connect', docker_network, 'RadonCTT'])

        if not exclude_sut:
            sut_docker_name = 'docker-compose_edge-router_1'
            sut_ip = Deployment.workaround_parse_ip(docker_network, sut_docker_name)
            current_app.logger.info(f'Determined SUT IP-address: {sut_ip}.')
            result_set['sut'] = sut_ip

        ti_docker_name = 'CTTAgent'
        subprocess.call(['docker', 'network', 'connect', docker_network, ti_docker_name])
        ti_ip = Deployment.workaround_parse_ip(docker_network, ti_docker_name)
        current_app.logger.info(f'Determined TI IP-address: {ti_ip}.')
        result_set['ti'] = ti_ip

        return result_set

    @classmethod
    def workaround_parse_ip(cls, docker_network, docker_name):
        ip_address_line = subprocess.getoutput(
            f'docker network inspect {docker_network} | grep {docker_name} -A 3 | grep "IPv4Address"')
        ip_address = re.search(ip_pattern, ip_address_line).group()
        return ip_address

    def undeploy(self):
        subprocess.call(['opera', 'undeploy'], cwd=self.sut_storage_path)
        subprocess.call(['opera', 'undeploy'], cwd=self.ti_storage_path)

    @property
    def base_storage_path(self):
        return self.storage_path

    @property
    def sut_storage_path(self):
        return os.path.join(self.storage_path, 'system_under_test')

    @property
    def ti_storage_path(self):
        return os.path.join(self.storage_path, 'test_infrastructure')

    @property
    def test_artifact(self):
        return TestArtifact.get_by_uuid(self.testartifact_uuid)

    @classmethod
    def get_parent_type(cls):
        return TestArtifact

    @classmethod
    def create(cls, testartifact_uuid):
        linked_testartifact = TestArtifact.get_by_uuid(testartifact_uuid)

        deployment = Deployment(linked_testartifact)
        deployment.deploy()

        # TODO: What to return here? Status of all deployments?
        return deployment

    @classmethod
    def get_all(cls):
        return Deployment.query.all()

    @classmethod
    def get_by_uuid(cls, get_uuid):
        return Deployment.query.filter_by(uuid=get_uuid).first()

    @classmethod
    def delete_by_uuid(cls, del_uuid):
        deployment = Deployment.query.filter_by(uuid=del_uuid)
        if deployment:
            from models.execution import Execution
            linked_executions = Execution.query.filter_by(deployment_uuid=del_uuid)
            for result in linked_executions:
                Execution.delete_by_uuid(result.uuid)

            deployment.delete()
            # rmtree(self.fq_storage_path)
            db_session.commit()
