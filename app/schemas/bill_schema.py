from marshmallow import Schema, fields, validate
from marshmallow.validate import Length

from app.schemas.bill_item_schema import BillItemCreateSchema, BillItemSchema
from app.schemas.person_schema import PersonSchema


class BillCreateSchema(Schema):
    buyer_id = fields.Int(required=True, validate=validate.Range(min=1))
    total_price = fields.Int(required=False)
    date = fields.Date(required=True, format='%Y-%m-%d')
    purchase_order = fields.Str(required=True, validate=Length(max=30))
    remarks = fields.Str(required=False)
    items = fields.List(fields.Nested(BillItemCreateSchema), required=True)


class BillResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    buyer_id = fields.Int(dump_only=True)
    total_price = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True, format='%Y-%m-%d')
    purchase_order = fields.Str(dump_only=True)
    remarks = fields.Str()


class BillListResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    total_price = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True, format='%Y-%m-%d')
    purchase_order = fields.Str(dump_only=True)
    remarks = fields.Str()
    buyer = fields.Nested(PersonSchema, dump_only=True)
    bill_items = fields.Nested(BillItemSchema, many=True, dump_only=True)


class BillUpdateSchema(Schema):
    remarks = fields.Str()


class BillQuerySchema(Schema):
    buyer_id = fields.Integer(validate=validate.Range(min=1))
    purchase_order = fields.String(validate=Length(max=30))
    start_date = fields.Date(format='%Y-%m-%d')
    end_date = fields.Date(format='%Y-%m-%d')
    min_total_price = fields.Float(validate=validate.Range(min=1))
    max_total_price = fields.Float(validate=validate.Range(min=1))
    search = fields.String()
    sort_by = fields.String(validate=validate.OneOf(['buyer_id', 'total_price', 'date']), load_default='date')
    sort_order = fields.String(validate=validate.OneOf(['asc', 'desc']), load_default='desc')
    limit = fields.Integer(load_default=20, validate=validate.Range(min=1))
    offset = fields.Integer(load_default=0, validate=validate.Range(min=0))
