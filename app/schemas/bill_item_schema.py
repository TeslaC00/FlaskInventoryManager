from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema


class BillItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    c_gst = fields.Float(required=True)
    s_gst = fields.Float(required=True)
    i_gst = fields.Float(required=True)
    bill_id = fields.Integer(required=True)
    product_part_no = fields.Integer(required=True)


class BillItemUpdateSchema(Schema):
    quantity = fields.Integer()
    price = fields.Float()
    c_gst = fields.Float()
    s_gst = fields.Float()
    i_gst = fields.Float()


class BillItemQuerySchema(QuerySchema):
    bill_id = fields.Integer()
    product_part_no = fields.Integer()
    sort_by = fields.String(
        validate=validate.OneOf(['quantity', 'price', 'c_gst', 's_gst', 'i_gst', 'bill_id', 'product_part_no']),
        load_default='id')
