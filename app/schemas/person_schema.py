from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema


# Used for Supplier and Buyer
class PersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    GST_No = fields.String(required=True)
    state_code = fields.Integer(required=True)
    state_name = fields.String(required=True)
    address = fields.String(allow_none=True)


class PersonUpdateSchema(Schema):
    name = fields.String()
    state_code = fields.Integer()
    state_name = fields.String()
    address = fields.String()


class PersonQuerySchema(QuerySchema):
    name = fields.String()
    GST_No = fields.String(validate=validate.Length(equal=15))
    state_code = fields.Integer(validate=validate.Length(min=1, max=28))
    state_name = fields.String()
    sort_by = fields.String(validate=validate.OneOf(['name', 'state_code', 'state_name']), missing=['name'])
