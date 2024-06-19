from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.api.utils import apply_sorting
from app.extensions import db
from app.logger import logger
from app.models import ProductionLog
from app.schemas.production_log_schema import ProductionLogSchema, ProductionLogQuerySchema, ProductionLogUpdateSchema

production_log_bp = Blueprint('production_log_bp', __name__)


@production_log_bp.route('/production_log')
class ProductionLogListResource(MethodView):
    @production_log_bp.response(200, ProductionLogSchema(many=True))
    @production_log_bp.arguments(ProductionLogQuerySchema, location='query')
    @production_log_bp.paginate()
    def get(self, query_args, pagination_parameters):
        logger.info('GET /production_logs called')
        logger.debug(f"Query Arguments={query_args}")

        query = ProductionLog.query

        # for filtering
        if 'product_part_no' in query_args:
            query = query.filter(ProductionLog.product_part_no.like(f"%{query_args['product_part_no']}%"))
        if 'start_date' in query_args:
            query = query.filter(ProductionLog.production_date >= query_args['start_date'])
        if 'end_date' in query_args:
            query = query.filter(ProductionLog.production_date <= query_args['end_date'])
        if 'min_quantity' in query_args:
            query = query.filter(ProductionLog.quantity_produced >= query_args['min_quantity'])
        if 'max_quantity' in query_args:
            query = query.filter(ProductionLog.quantity_produced <= query_args['max_quantity'])
        # for searching
        # for sorting
        production_logs = apply_sorting(query, query_args, pagination_parameters)
        logger.info(f"Found {pagination_parameters.item_count} production_logs")
        logger.debug(f"Returned production_logs: {production_logs}")
        return production_logs

    @production_log_bp.response(201, ProductionLogSchema)
    @production_log_bp.arguments(ProductionLogSchema)
    def post(self, new_production_log_data):
        logger.info('POST /production_logs called')
        logger.debug(f"Creating new production log with args: {new_production_log_data}")

        try:
            new_production_log = ProductionLog(**new_production_log_data)
            db.session.add(new_production_log)
            db.session.commit()
            logger.info(f"New production log created with ID {new_production_log.id}")
            return new_production_log
        except Exception as e:
            logger.error(f"Error creating production log: {e}")
            abort(500, message="An error occurred while creating the production log")


@production_log_bp.route('/production_log/<int:production_log_id>')
class ProductionLogResource(MethodView):
    @production_log_bp.response(200, ProductionLogSchema)
    def get(self, production_log_id):
        logger.info(f"GET /production_logs/{production_log_id} called")
        production_log = ProductionLog.query.get_or_404(production_log_id, description="Production log not found")
        logger.info(f"Found production log with ID {production_log_id}")
        return production_log

    @production_log_bp.response(200, ProductionLogSchema)
    @production_log_bp.arguments(ProductionLogUpdateSchema)
    def put(self, update_production_log_data, production_log_id):
        logger.info(f"PUT /production_logs/{production_log_id} called")
        logger.debug(f"Updating production log {production_log_id} with args: {update_production_log_data}")

        production_log = ProductionLog.query.get_or_404(production_log_id, description="Production log not found")
        for key, value in update_production_log_data.items():
            setattr(production_log, key, value)

        try:
            db.session.commit()
            logger.info(f"Production log {production_log_id} updated")
            return production_log
        except Exception as e:
            logger.error(f"Error updating production log {production_log_id}: {e}")
            abort(500, message="An error occurred while updating the production log")

    @production_log_bp.response(204)
    def delete(self, production_log_id):
        logger.info(f"DELETE /production_logs/{production_log_id} called")
        production_log = ProductionLog.query.get_or_404(production_log_id, description="Production log not found")
        try:
            db.session.delete(production_log)
            db.session.commit()
            logger.info(f"Production log {production_log_id} deleted")
            return {'message': 'Production log deleted'}
        except Exception as e:
            logger.error(f"Error deleting production log {production_log_id}: {e}")
            abort(500, message="An error occurred while deleting the production log")
