from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema
from app.schemas.unit_schema import UnitSchema


class MaterialSchema(Schema):
    part_no = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)


class MaterialCreateSchema(Schema):
    unit_id = fields.Integer(required=True)
    name = fields.String(required=True)
    quantity = fields.Integer(required=True)


class MaterialResponseSchema(Schema):
    part_no = fields.Integer(dump_only=True)
    unit = fields.Nested(UnitSchema, dump_only=True)
    name = fields.String(dump_only=True)
    quantity = fields.Integer(dump_only=True)


class MaterialUpdateSchema(Schema):
    quantity = fields.Integer()
    unit_id = fields.Integer()


class MaterialQuerySchema(QuerySchema):
    name = fields.String()
    unit_id = fields.Integer()
    min_quantity = fields.Integer()
    max_quantity = fields.Integer()
    sort_by = fields.String(validate=validate.OneOf(['name', 'quantity']), load_default='name')
