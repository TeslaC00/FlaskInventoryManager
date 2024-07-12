from marshmallow import Schema, fields, validate

from app.schemas.challan_item_schema import ChallanItemSchema, ChallanItemCreateSchema
from app.schemas.person_schema import PersonSchema
from app.schemas.query_schema import QuerySchema


class ChallanCreateSchema(Schema):
    challan_no = fields.Integer(required=True)
    supplier_id = fields.Integer(required=True)
    total_price = fields.Float(required=True)
    date = fields.Date(required=True, format='%Y-%m-%d')
    remarks = fields.String(allow_none=True)
    items = fields.List(fields.Nested(ChallanItemCreateSchema), required=True)


class ChallanResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    challan_no = fields.Integer(dump_only=True)
    supplier_id = fields.Integer(dump_only=True)
    total_price = fields.Float(dump_only=True)
    date = fields.Date(dump_only=True, format='%Y-%m-%d')
    remarks = fields.String(dump_only=True)


class ChallanListResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    challan_no = fields.Integer(dump_only=True)
    total_price = fields.Float(dump_only=True)
    date = fields.Date(dump_only=True, format='%Y-%m-%d')
    remarks = fields.String(dump_only=True)
    supplier = fields.Nested(PersonSchema, dump_only=True)
    challan_items = fields.Nested(ChallanItemSchema, many=True, dump_only=True)


class ChallanUpdateSchema(Schema):
    remarks = fields.String()


class ChallanQuerySchema(QuerySchema):
    challan_no = fields.Integer()
    supplier_id = fields.Integer()
    start_date = fields.DateTime(format='%Y-%m-%d')
    end_date = fields.DateTime(format='%Y-%m-%d')
    min_total_price = fields.Float()
    max_total_price = fields.Float()
    sort_by = fields.String(validate=validate.OneOf(['challan_no', 'supplier_id', 'total_price', 'date']),
                            load_default='date')
