from marshmallow import Schema, fields, validate


class BillSchema(Schema):
    id = fields.Int(dump_only=True)
    buyer_id = fields.Int(dump_only=True)
    total_price = fields.Int(required=True)
    date = fields.Date(dump_only=True, format='%Y-%m-%d')
    purchase_order = fields.Str(dump_only=True)
    remarks = fields.Str()


class BillUpdateSchema(Schema):
    total_price = fields.Int()
    remarks = fields.Str()


class BillQuerySchema(Schema):
    buyer_id = fields.Integer()
    purchase_order = fields.String()
    start_date = fields.DateTime(format='%Y-%m-%d')
    end_date = fields.DateTime(format='%Y-%m-%d')
    min_total_price = fields.Float()
    max_total_price = fields.Float()
    search = fields.String()
    sort_by = fields.String(validate=validate.OneOf(['buyer_id', 'total_price', 'date']), missing='date')
    sort_order = fields.String(validate=validate.OneOf(['asc', 'desc']), missing='desc')
    limit = fields.Integer(missing=20)
    offset = fields.Integer(missing=0)
