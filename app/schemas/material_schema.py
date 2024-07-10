from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema
from app.schemas.unit_schema import UnitSchema


class MaterialSchema(Schema):
    part_no = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    quantity = fields.Integer(required=True)


class MaterialCreateSchema(MaterialSchema):
    unit_id = fields.Integer(required=True)


class MaterialResponseSchema(MaterialSchema):
    unit = fields.Nested(UnitSchema, only=('name',), required=True)


class MaterialUpdateSchema(Schema):
    quantity = fields.Integer()
    unit_id = fields.Integer()


class MaterialQuerySchema(QuerySchema):
    name = fields.String()
    unit_id = fields.Integer()
    min_quantity = fields.Integer()
    max_quantity = fields.Integer()
    sort_by = fields.String(validate=validate.OneOf(['name', 'quantity']), load_default='name')
