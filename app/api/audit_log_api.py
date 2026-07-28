from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app import logger
from app.services.audit_log_service import AuditLogService
from app.errors.not_found_error import NotFoundError
from app.schemas.audit_log_schema import AuditLogSchema, AuditLogQuerySchema

audit_log_bp = Blueprint('audit_log', __name__, description='Operations on audit log')


@audit_log_bp.route('/audit_log')
class AuditLogListResource(MethodView):
    @audit_log_bp.response(200, AuditLogSchema(many=True))
    @audit_log_bp.arguments(AuditLogQuerySchema, location='query')
    @audit_log_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /audit_log called')
        logger.info(f'query_args: {filters}')
        try:
            audit_logs = AuditLogService.get_all_audit_logs(pagination_parameters.page, pagination_parameters.page_size,
                                                            **filters)
            pagination_parameters.item_count = audit_logs.total
            logger.info(f"Found {pagination_parameters.item_count} audit_logs")
            logger.debug(f"Returned audit_logs: {audit_logs}")
            return audit_logs
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e, message=str(e))

    @audit_log_bp.response(201, AuditLogSchema)
    @audit_log_bp.arguments(AuditLogSchema)
    def post(self, data):
        logger.info('POST /audit_log called')
        logger.debug(f"Creating new bill with args: {data}")
        try:
            audit_log = AuditLogService.add_audit_log(**data)
            logger.info(f"New AuditLog created with ID {audit_log.id}")
            return audit_log
        except ValueError as ve:
            logger.error(f"Error creating audit_log: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating audit_log: {e}")
            abort(500, e)


@audit_log_bp.route('/audit_log/<int:audit_log_id>')
class AuditLogResource(MethodView):
    @audit_log_bp.response(200, AuditLogSchema)
    def get(self, audit_log_id):
        logger.info(f'GET /audit_log/{audit_log_id} called')
        try:
            audit_log = AuditLogService.get_audit_log_by_id(audit_log_id)
            logger.info(f"Found audit_log with ID {audit_log_id}")
            return audit_log
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)
