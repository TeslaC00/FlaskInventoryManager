from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.services.production_log_service import ProductionLogService
from app.schemas.production_log_schema import ProductionLogSchema, ProductionLogQuerySchema, ProductionLogUpdateSchema

production_log_bp = Blueprint('production_log_bp', __name__)


@production_log_bp.route('/production_log')
class ProductionLogListResource(MethodView):
    @production_log_bp.response(200, ProductionLogSchema(many=True))
    @production_log_bp.arguments(ProductionLogQuerySchema, location='query')
    @production_log_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /production_logs called')
        logger.debug(f"Query Arguments={filters}")

        try:
            production_logs = ProductionLogService.get_all_production_logs(pagination_parameters.page,
                                                                           pagination_parameters.page_size, **filters)
            pagination_parameters.item_count = production_logs.total
            logger.info(f"Found {pagination_parameters.item_count} production_logs")
            logger.debug(f"Returned production_logs: {production_logs}")
            return production_logs
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @production_log_bp.response(201, ProductionLogSchema)
    @production_log_bp.arguments(ProductionLogSchema)
    def post(self, data):
        logger.info('POST /production_logs called')
        logger.debug(f"Creating new production log with args: {data}")

        try:
            production_log = ProductionLogService.add_production_log(**data)
            logger.info(f"New ProductionLog created with ID {production_log.id}")
            return production_log
        except ValueError as ve:
            logger.error(f"Error creating production_log: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating production_log: {e}")
            abort(500, e)


@production_log_bp.route('/production_log/<int:production_log_id>')
class ProductionLogResource(MethodView):
    @production_log_bp.response(200, ProductionLogSchema)
    def get(self, production_log_id):
        logger.info(f"GET /production_logs/{production_log_id} called")
        try:
            production_log = ProductionLogService.get_production_log_by_id(production_log_id)
            logger.info(f"Found production_log with ID {production_log_id}")
            return production_log
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @production_log_bp.response(200, ProductionLogSchema)
    @production_log_bp.arguments(ProductionLogUpdateSchema)
    def put(self, data, production_log_id):
        logger.info(f"PUT /production_logs/{production_log_id} called")
        logger.debug(f"Updating production log {production_log_id} with args: {data}")

        try:
            production_log = ProductionLogService.update_production_log(production_log_id, data)
            logger.info(f"ProductionLog {production_log_id} updated")
            return production_log
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating production_log {production_log_id}: {e}")
            abort(500, e)

    @production_log_bp.response(204)
    def delete(self, production_log_id):
        logger.info(f"DELETE /production_logs/{production_log_id} called")
        try:
            ProductionLogService.delete_production_log(production_log_id)
            logger.info(f"ProductionLog {production_log_id} deleted")
            return {'message': 'ProductionLog deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting production_log {production_log_id}: {e}")
            abort(500, e)
