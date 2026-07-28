from marshmallow import Schema, fields

from app.schemas.query_schema import QuerySchema


class RoleCreateSchema(Schema):
    name = fields.Str(required=True)
    permissions = fields.List(fields.Str(), required=True)
    description = fields.Str()


class RoleUpdateSchema(Schema):
    permissions = fields.List(fields.Str())
    description = fields.Str()


class RoleListResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)


class RoleResponseSchema(RoleListResponseSchema):
    permissions = fields.List(fields.Str(), dump_only=True)


class RoleQuerySchema(QuerySchema):
    pass
