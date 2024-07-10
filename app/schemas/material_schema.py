from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema
from app.schemas.unit_schema import UnitSchema


class MaterialSchema(Schema):
    part_no = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    quantity = fields.Integer(required=True)


class MaterialCreateSchema(MaterialSchema):
    unit = fields.Nested(UnitSchema, only=('id', 'name'), required=True)


class MaterialResponseSchema(MaterialSchema):
    unit = fields.Nested(UnitSchema, only=('id', 'name'), required=True)


class MaterialUpdateSchema(Schema):
    quantity = fields.Integer(required=True)
    unit = fields.Nested(UnitSchema, only=('id', 'name'))


class MaterialQuerySchema(QuerySchema):
    name = fields.String()
    unit = fields.Nested(UnitSchema, only=('id', 'name'))
    min_quantity = fields.Integer()
    max_quantity = fields.Integer()
    sort_by = fields.String(validate=validate.OneOf(['name', 'quantity']), load_default='name')
