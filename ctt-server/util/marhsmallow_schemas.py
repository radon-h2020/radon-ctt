from marshmallow import Schema, fields


class ProjectSchema(Schema):
    uuid = fields.Str()
    name = fields.Str()
    repository_url = fields.Str()