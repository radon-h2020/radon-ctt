import os
import shutil
import uuid

from flask import current_app
from sqlalchemy import Column, String, ForeignKey
from straight.plugin.loaders import ModuleLoader

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
    results_file: str
    storage_path: str

    uuid = Column(String, primary_key=True)
    deployment_uuid = Column(String, ForeignKey('deployment.uuid'), nullable=False)
    agent_configuration_uuid = Column(String)
    agent_execution_uuid = Column(String)
    sut_ip_address = Column(String)
    ti_ip_address = Column(String)
    results_file = Column(String)
    storage_path = Column(String)

    results_file_name = 'results.zip'

    def __init__(self, deployment):
        if deployment:
            self.uuid = str(uuid.uuid4())
            self.deployment = deployment
            self.deployment_uuid = deployment.uuid
            self.storage_path = os.path.join(BasePath, self.__tablename__, self.uuid)
            self.plugin = None
            self.test_artifact = deployment.test_artifact

            plugins_available = ModuleLoader().load('plugins')
            for p in plugins_available:
                if p.plugin_type == self.test_artifact.plugin:
                    self.plugin = p

            if not self.plugin:
                raise LookupError(f"Could not find matching plugin for '{self.test_artifact.plugin}'.")

            db_session.add(self)
            db_session.commit()

            if not os.path.exists(self.fq_storage_path):
                os.makedirs(self.fq_storage_path)
        else:
            raise Exception(f'Linked entities do not exist.')

    def __repr__(self):
        return '<Execution UUID=%r, AGENT_CONFIG_UUID=%r, AGENT_EXEC_UUID=%r>' % \
               (self.uuid, self.agent_configuration_uuid, self.agent_execution_uuid)

    @property
    def fq_storage_path(self):
        return os.path.join(BasePath, self.storage_path)

    @property
    def fq_result_storage_path(self):
        return os.path.join(self.fq_storage_path, self.results_file_name)

    @property
    def result_storage_path(self):
        return os.path.join(self.storage_path, self.results_file_name)

    @property
    def system_under_test_ip(self):
        return self.sut_ip_address

    @property
    def test_infrastructure_ip(self):
        return self.ti_ip_address

    def configure(self):
        test_artifact_yaml_policy = self.test_artifact.policy_yaml
        test_artifact_storage_path = self.test_artifact.fq_storage_path

        config_uuid = self.plugin.configure(self.deployment.hostname_ti,
                                            test_artifact_yaml_policy,
                                            test_artifact_storage_path,
                                            sut_hostname=self.deployment.hostname_sut)

        self.agent_configuration_uuid = config_uuid
        return config_uuid

    def execute(self, config_uuid):
        execution_uuid = self.plugin.execute(self.deployment.hostname_ti,
                                             config_uuid)
        self.agent_execution_uuid = execution_uuid
        return execution_uuid

    def get_results(self, execution_uuid):
        if execution_uuid:
            temp_results_file = self.plugin.get_results(self.deployment.hostname_ti, execution_uuid)
            shutil.move(temp_results_file, self.fq_result_storage_path)

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
            if exec_uuid:
                execution.get_results(exec_uuid)
                db_session.add(execution)
                db_session.commit()
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
