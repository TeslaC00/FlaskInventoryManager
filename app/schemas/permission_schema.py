from marshmallow import Schema, fields


class PermissionSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class PermissionResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
