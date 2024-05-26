from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models import AuditLog, ActionType

# Define output fields for marshalling
audit_log_fields = {
    'audit_id': fields.Integer(attribute='id'),
    'table_name': fields.String,
    'table_primary_key': fields.String,
    'column_name': fields.String,
    'old_value': fields.String,
    'new_value': fields.String,
    'username': fields.String,
    'change_timestamp': fields.DateTime,
    'action_type': fields.String(attribute='action_type.name'),
    'remarks': fields.String
}

api = Api(create_app)


def abort_if_audit_log_not_found(audit_log_id):
    audit_log = AuditLog.query.get(audit_log_id)
    if not audit_log:
        abort(404, message="Audit log not found")
    return audit_log


class AuditLogResource(Resource):
    @marshal_with(audit_log_fields)
    def get(self, id=None):
        if id:
            audit_log = abort_if_audit_log_not_found(id)
            return audit_log, 200
        logs = AuditLog.query.order_by(AuditLog.change_timestamp.desc()).all()
        return logs, 200

    @marshal_with(audit_log_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('table_name', type=str, required=True, help='Table name is required')
        parser.add_argument('table_primary_key', type=str, required=True, help='Table primary key is required')
        parser.add_argument('column_name', type=str, required=True, help='Column name is required')
        parser.add_argument('old_value', type=str, required=True, help='Old value is required')
        parser.add_argument('new_value', type=str, required=True, help='New value is required')
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('action_type', type=int, required=True, help='Action type is required')
        parser.add_argument('remarks', type=str)
        args = parser.parse_args()

        new_log = AuditLog(
            table_name=args['table_name'],
            table_primary_key=args['table_primary_key'],
            column_name=args['column_name'],
            old_value=args['old_value'],
            new_value=args['new_value'],
            username=args['username'],
            action_type=ActionType(args['action_type']),
            remarks=args.get('remarks')
        )
        db.session.add(new_log)
        db.session.commit()
        return new_log, 201


class AuditLogFilterResource(Resource):
    @marshal_with(audit_log_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_date', type=str, required=True, help='Start date is required')
        parser.add_argument('end_date', type=str, required=True, help='End date is required')
        args = parser.parse_args()

        try:
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(args['end_date'], '%Y-%m-%d')
        except ValueError:
            abort(400, message="Dates must be in YYYY-MM-DD format")

        logs = AuditLog.query \
            .filter(AuditLog.change_timestamp >= start_date) \
            .filter(AuditLog.change_timestamp <= end_date) \
            .order_by(AuditLog.change_timestamp.desc()).all()

        return logs, 200


api.add_resource(AuditLogResource, '/audit_logs', '/audit_logs/<int:id>')
api.add_resource(AuditLogFilterResource, '/audit_logs/filter')
