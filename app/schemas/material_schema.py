from marshmallow import Schema, fields, validate

from app.models.enums import UnitType
from app.schemas.query_schema import QuerySchema


class MaterialSchema(Schema):
    part_no = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    unit = fields.String(required=True, validate=validate.OneOf([unit.value for unit in UnitType]))
    quantity = fields.Integer(required=True)


class MaterialUpdateSchema(Schema):
    quantity = fields.Integer(required=True)


class MaterialQuerySchema(QuerySchema):
    name = fields.String()
    unit = fields.String(validate=validate.OneOf([unit.value for unit in UnitType]))
    min_quantity = fields.Integer()
    max_quantity = fields.Integer()
    sort_by = fields.String(validate=validate.OneOf(['name', 'quantity', 'unit']), missing='name')
