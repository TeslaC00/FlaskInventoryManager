from marshmallow import Schema, fields, validate


class QuerySchema(Schema):
    search = fields.String()
    sort_order = fields.String(validate=validate.OneOf(['asc', 'desc']), load_default='desc')
