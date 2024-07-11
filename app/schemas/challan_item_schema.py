from marshmallow import Schema, fields, validate

from app.schemas.material_schema import MaterialSchema
from app.schemas.query_schema import QuerySchema


class ChallanItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    price = fields.Float(dump_only=True)
    quantity = fields.Integer(dump_only=True)
    material = fields.Nested(MaterialSchema, dump_only=True)


class ChallanItemCreateSchema(Schema):
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)
    challan_id = fields.Integer(required=True)
    material_part_no = fields.Integer(required=True)


class ChallanItemResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    price = fields.Float(dump_only=True)
    quantity = fields.Integer(dump_only=True)
    challan_id = fields.Integer(dump_only=True)
    material_part_no = fields.Integer(dump_only=True)


class ChallanItemUpdateSchema(Schema):
    price = fields.Float()
    quantity = fields.Integer()


# maybe redundant
class ChallanQuerySchema(QuerySchema):
    challan_id = fields.Integer()
    material_part_no = fields.Integer()
    sort_by = fields.String(
        validate=validate.OneOf(['quantity', 'price', 'challan_id', 'material_part_no']),
        load_default='id')
