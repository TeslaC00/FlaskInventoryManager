from marshmallow import Schema, fields


class RoleSchema(Schema):
    id = fields.Integer(dump_only=True)


class RoleCreateSchema(RoleSchema):
    name = fields.Str(required=True)
    description = fields.Str()
    permissions = fields.List(fields.Str())


class RoleResponseSchema(RoleSchema):
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    permissions = fields.List(fields.Str(), dump_only=True)
