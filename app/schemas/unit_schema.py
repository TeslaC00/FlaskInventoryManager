from marshmallow import Schema, fields


class UnitSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
