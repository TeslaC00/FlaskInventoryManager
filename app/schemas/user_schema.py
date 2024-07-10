from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema


class UserSchema(Schema):
    id = fields.Int(dump_only=True)


class UserResponseSchema(UserSchema):
    email = fields.Email(dump_only=True)
    username = fields.Str(dump_only=True)
    active = fields.Bool(dump_only=True)
    last_login = fields.DateTime(dump_only=True)


class UserCreateSchema(UserSchema):
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=8))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    security_question = fields.Str(required=True, validate=validate.Length(max=255))
    security_answer = fields.Str(required=True, validate=validate.Length(max=255))
    roles = fields.List(fields.Str(validate=validate.Length(max=255)))


class UserUpdateSchema(Schema):
    active = fields.Bool()


# add more query params
class UserQuerySchema(QuerySchema):
    email = fields.Email()
    username = fields.Str()
    active = fields.Bool()
    sort_by = fields.String(validate=validate.OneOf(['username', 'email']), load_default='username')


class UserRoleSchema(Schema):
    pass
