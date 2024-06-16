from flask import request
from flask_restful import Resource, abort, fields, marshal_with
from datetime import datetime
from app.extensions import db
from app.models.audit_log import AuditLog
from app.models.enums import ActionType
from app.logger import logger

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
    'action_type': fields.String(attribute=lambda x: x.action_type.value),
    'remarks': fields.String
}


def abort_if_audit_log_not_found(audit_log_id):
    audit_log = AuditLog.query.get(audit_log_id)
    if not audit_log:
        logger.error(f"Audit log with ID {audit_log_id} not found")
        abort(404, message="Audit log not found")
    return audit_log


class AuditLogResource(Resource):
    @marshal_with(audit_log_fields)
    def get(self, audit_id=None):
        if audit_id:
            audit_log = abort_if_audit_log_not_found(audit_id)
            return audit_log, 200

        # Handle pagination
        limit = request.args.get('limit', default=20, type=int)
        offset = request.args.get('offset', default=0, type=int)

        logs = AuditLog.query.order_by(AuditLog.change_timestamp.desc()).offset(offset).limit(limit).all()
        logger.info(f"Retrieved {len(logs)} audit logs with limit={limit} and offset={offset}")
        return logs, 200

    @marshal_with(audit_log_fields)
    def post(self):
        json_data = request.get_json()
        if not json_data:
            logger.error("No input data provided")
            return {"message": "No input data provided"}, 400

        required_fields = ['table_name', 'table_primary_key', 'column_name', 'old_value', 'new_value', 'username',
                           'action_type']
        for field in required_fields:
            if field not in json_data:
                logger.error(f"{field} is required")
                return {"message": f"{field} is required"}, 400

        try:
            new_log = AuditLog(
                table_name=json_data['table_name'],
                table_primary_key=json_data['table_primary_key'],
                column_name=json_data['column_name'],
                old_value=json_data['old_value'],
                new_value=json_data['new_value'],
                username=json_data['username'],
                action_type=ActionType(json_data['action_type']),
                remarks=json_data.get('remarks')
            )
            db.session.add(new_log)
            db.session.commit()
            logger.info(f"New audit log created with ID {new_log.id}")
            return new_log, 201
        except Exception as e:
            logger.error(f"Error creating audit log: {e}", exc_info=True)
            db.session.rollback()
            return {"message": "An error occurred while creating the audit log"}, 500


class AuditLogFilterResource(Resource):
    @marshal_with(audit_log_fields)
    def get(self):
        json_data = request.get_json()
        if not json_data:
            logger.error("No input data provided")
            return {"message": "No input data provided"}, 400

        if 'start_date' not in json_data or 'end_date' not in json_data:
            logger.error("Start date and end date are required")
            return {"message": "Start date and end date are required"}, 400

        try:
            start_date = datetime.strptime(json_data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(json_data['end_date'], '%Y-%m-%d')
        except ValueError:
            logger.error("Dates must be in YYYY-MM-DD format")
            return {"message": "Dates must be in YYYY-MM-DD format"}, 400

        # Handle pagination
        limit = request.args.get('limit', default=20, type=int)
        offset = request.args.get('offset', default=0, type=int)

        logs = AuditLog.query \
            .filter(AuditLog.change_timestamp >= start_date) \
            .filter(AuditLog.change_timestamp <= end_date) \
            .order_by(AuditLog.change_timestamp.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()

        logger.info(
            f"Retrieved {len(logs)} audit logs between {start_date} and {end_date} with limit={limit} and offset={offset}")
        return logs, 200

# Add resource routes
# api.add_resource(AuditLogResource, '/audit_logs', '/audit_logs/<int:audit_id>')
# api.add_resource(AuditLogFilterResource, '/audit_logs/filter')
