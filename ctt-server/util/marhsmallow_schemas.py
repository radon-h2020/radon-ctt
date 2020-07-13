from marshmallow import Schema, fields


class ProjectSchema(Schema):
    uuid = fields.Str()
    name = fields.Str()
    repository_url = fields.Str()


class TestArtifactSchema(Schema):
    uuid = fields.Str()
    # commit_hash = fields.Str()
    # sut_tosca_path = fields.Str()
    # ti_tosca_path = fields.Str()
    project_uuid = fields.Str()


class DeploymentSchema(Schema):
    uuid = fields.Str()
    testartifact_uuid = fields.Str()


class ExecutionSchema(Schema):
    uuid = fields.Str()
    agent_configuration_uuid = fields.Str()
    agent_execution_uuid = fields.Str()


class ResultSchema(Schema):
    uuid = fields.Str()
    execution_uuid = fields.Str()
    results_file = fields.Str()
