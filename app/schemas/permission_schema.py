from marshmallow import Schema, fields


class PermissionSchema(Schema):
    name = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
