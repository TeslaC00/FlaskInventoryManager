from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema


class ChallanSchema(Schema):
    id = fields.Integer(dump_only=True)
    challan_no = fields.Integer(required=True)
    supplier_id = fields.Integer(required=True)
    total_price = fields.Float(required=True)
    date = fields.Date(required=True, format='%Y-%m-%d')
    remarks = fields.String(allow_none=True)


class ChallanUpdateSchema(Schema):
    total_price = fields.Float()
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
