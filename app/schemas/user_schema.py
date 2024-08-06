from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema
from app.schemas.role_schema import RoleListResponseSchema, RoleResponseSchema


class UserListResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(dump_only=True)
    username = fields.Str(dump_only=True)
    active = fields.Bool(dump_only=True)
    last_login = fields.DateTime(dump_only=True)
    roles = fields.Nested(RoleListResponseSchema, many=True)


class UserResponseSchema(UserListResponseSchema):
    roles = fields.Nested(RoleResponseSchema, many=True)


class UserSecurityQuestionSchema(Schema):
    id = fields.Int(required=True)
    answer = fields.Str(required=True)


class UserCreateSchema(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=8))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    questions = fields.Nested(UserSecurityQuestionSchema, many=True)
    roles = fields.List(fields.Str(validate=validate.Length(max=255)), required=True)


class UserUpdateSchema(Schema):
    active = fields.Bool()
    role_ids = fields.List(fields.Integer())


# add more query params
class UserQuerySchema(QuerySchema):
    email = fields.Email()
    username = fields.Str()
    active = fields.Bool()
    sort_by = fields.String(validate=validate.OneOf(['username', 'email']), load_default='username')
