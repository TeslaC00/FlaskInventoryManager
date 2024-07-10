from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema


class ProductSchema(Schema):
    part_no = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    unit_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    c_gst = fields.Float(required=True)
    s_gst = fields.Float(required=True)
    i_gst = fields.Float(required=True)


class ProductUpdateSchema(Schema):
    quantity = fields.Integer()
    price = fields.Float()
    c_gst = fields.Float()
    s_gst = fields.Float()
    i_gst = fields.Float()


class ProductQuerySchema(QuerySchema):
    name = fields.String()
    unit_id = fields.Integer()
    min_quantity = fields.Integer()
    max_quantity = fields.Integer()
    min_price = fields.Float()
    max_price = fields.Float()
    min_c_gst = fields.Float()
    max_c_gst = fields.Float()
    min_s_gst = fields.Float()
    max_s_gst = fields.Float()
    min_i_gst = fields.Float()
    max_i_gst = fields.Float()
    sort_by = fields.String(validate=validate.OneOf(['name', 'unit', 'quantity', 'price', 'c_gst', 's_gst', 'i_gst']),
                            load_default='name')
