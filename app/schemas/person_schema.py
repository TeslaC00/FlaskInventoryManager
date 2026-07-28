from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema


class StateSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(dump_only=True)
    abbreviation = fields.Str(dump_only=True)


# Used for Supplier and Buyer
class PersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)


class PersonCreateSchema(Schema):
    name = fields.String(required=True)
    GST_No = fields.String(required=True)
    state_code = fields.Integer(required=True)
    address = fields.String(allow_none=True)


class PersonResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    GST_No = fields.String(dump_only=True)
    state = fields.Nested(StateSchema, dump_only=True)
    address = fields.String(dump_only=True)


class PersonUpdateSchema(Schema):
    name = fields.String()
    state_code = fields.Integer()
    address = fields.String()


class PersonFilterSchema(QuerySchema):
    name = fields.String()
    GST_No = fields.String(validate=validate.Length(equal=15))
    state_code = fields.Integer(validate=validate.Range(min=1, max=37))
    state_name = fields.String()
    sort_by = fields.String(validate=validate.OneOf(['name', 'state_code', 'state_name']), load_default='name')
