from marshmallow import Schema, fields


class SecurityQuestionListResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    question = fields.String(dump_only=True)
