from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app import logger
from app.api.utils import apply_sorting, generate_meta
from app.extensions import db
from app.models.audit_log import AuditLog
from app.schemas.audit_log_schema import AuditLogSchema, AuditLogQuerySchema

audit_log_bp = Blueprint('audit_log', __name__, description='Operations on audit log')


@audit_log_bp.route('/audit_log')
class AuditLogListResource(MethodView):
    @audit_log_bp.response(200, AuditLogSchema(many=True))
    @audit_log_bp.arguments(AuditLogQuerySchema, location='query')
    def get(self, query_args):
        logger.info('GET /audit_log called')
        logger.info(f'query_args: {query_args}')

        query = AuditLog.query
        # for filtering
        if 'table_name' in query_args:
            query = query.filter(AuditLog.table_name.like(f"%{query_args['table_name']}%"))
        if 'table_primary_key' in query_args:
            query = query.filter(AuditLog.table_primary_key.like(f"%{query_args['table_primary_key']}%"))
        if 'column_name' in query_args:
            query = query.filter(AuditLog.column_name.like(f"%{query_args['column_name']}%"))
        if 'old_value' in query_args:
            query = query.filter(AuditLog.old_value.like(f"%{query_args['old_value']}%"))
        if 'new_value' in query_args:
            query = query.filter(AuditLog.new_value.like(f"%{query_args['new_value']}%"))
        if 'username' in query_args:
            query = query.filter(AuditLog.username.like(f"%{query_args['username']}%"))
        if 'start_timestamp' in query_args:
            query = query.filter(AuditLog.change_timestamp >= query_args['start_timestamp'])
        if 'end_timestamp' in query_args:
            query = query.filter(AuditLog.change_timestamp <= query_args['end_timestamp'])
        if 'action_type' in query_args:
            query = query.filter(AuditLog.action_type.like(f"%{query_args['action_type']}%"))
        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                AuditLog.table_name.like(search),
                AuditLog.username.like(search),
                AuditLog.remarks.like(search)
            ))
        # for sorting
        audit_logs, records_count = apply_sorting(query, query_args)
        logger.info(f'Found {records_count} audit logs')

        meta = generate_meta(records_count, query_args)
        return audit_logs, {'meta': meta}

    @audit_log_bp.response(201, AuditLogSchema)
    @audit_log_bp.arguments(AuditLogSchema)
    def post(self, new_audit_log_data):
        logger.info('POST /audit_log called')
        logger.debug(f"Creating new bill with args: {new_audit_log_data}")
        try:
            new_log = AuditLog(**new_audit_log_data)
            db.session.add(new_log)
            db.session.commit()
            logger.info(f"New bill created with ID {new_log.id}")
            return new_log
        except Exception as e:
            logger.error(f"Error creating audit log: {e}")
            abort(500, message="An error occurred while creating the audit log")


@audit_log_bp.route('/audit_log/<int:audit_log_id>')
class AuditLogResource(MethodView):
    @audit_log_bp.response(200, AuditLogSchema)
    def get(self, audit_log_id):
        logger.info(f'GET /audit_log/{audit_log_id} called')
        audit_log = AuditLog.query.get_or_404(audit_log_id)
        logger.info(f"Found audit log with ID {audit_log_id}")
        return audit_log
