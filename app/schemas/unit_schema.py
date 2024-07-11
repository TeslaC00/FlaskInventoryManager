from marshmallow import Schema, fields


class UnitSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()
