from marshmallow import Schema, fields, validate


class QuerySchema(Schema):
    search = fields.String()
    sort_order = fields.String(validate=validate.OneOf(['asc', 'desc']), missing='desc')
    limit = fields.Integer(missing=20)
    page = fields.Integer(missing=0)
