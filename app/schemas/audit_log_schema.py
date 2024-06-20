from marshmallow import Schema, fields, validate

from app.models.enums import ActionType
from app.schemas.query_schema import QuerySchema


class AuditLogSchema(Schema):
    id = fields.Integer(dump_only=True)
    table_name = fields.String(dump_only=True)
    table_primary_key = fields.String(dump_only=True)
    column_name = fields.String(dump_only=True)
    old_value = fields.String(dump_only=True)
    new_value = fields.String(dump_only=True)
    username = fields.String(dump_only=True)
    change_timestamp = fields.DateTime(dump_only=True)
    action_type = fields.String(dump_only=True, validate=validate.OneOf([action.value for action in ActionType]))
    remarks = fields.String(dump_only=True)


class AuditLogQuerySchema(QuerySchema):
    table_name = fields.String()
    table_primary_key = fields.String()
    column_name = fields.String()
    old_value = fields.String()
    new_value = fields.String()
    username = fields.String()
    start_timestamp = fields.DateTime()
    end_timestamp = fields.DateTime()
    action_type = fields.String(validate=validate.OneOf([action.value for action in ActionType]))
    sort_by = fields.String(validate=validate.OneOf(
        ['change_timestamp', 'table_name', 'table_primary_key', 'column_name', 'old_value', 'new_value', 'username']),
                            load_default='change_timestamp')
