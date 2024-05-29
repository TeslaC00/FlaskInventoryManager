from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from app.extensions import db
from app.models import ProductionLog
from app.logger import logger
from flask_restful import fields

production_log_fields = {
    'id': fields.Integer,
    'production_date': fields.DateTime(dt_format='iso8601'),
    'product_part_no': fields.Integer,
    'quantity_produced': fields.Integer
}


class ProductionLogListResource(Resource):
    @marshal_with(production_log_fields)
    def get(self):
        logger.info('GET /production_logs called')

        # for filtering
        product_part_no = request.args.get('product_part_no', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # for sorting
        sort_by = request.args.get('sort_by', 'production_date')
        limit = request.args.get('limit', type=int, default=20)
        offset = request.args.get('offset', type=int, default=0)

        query = ProductionLog.query
        if product_part_no is not None:
            query = query.filter_by(product_part_no=product_part_no)
        if start_date is not None:
            query = query.filter(ProductionLog.production_date >= start_date)
        if end_date is not None:
            query = query.filter(ProductionLog.production_date <= end_date)

        production_logs = query.order_by(sort_by).offset(offset).limit(limit).all()
        logger.info(f"Found {len(production_logs)} production logs")
        return production_logs, 200

    @marshal_with(production_log_fields)
    def post(self):
        logger.info('POST /production_logs called')
        parser = reqparse.RequestParser()
        parser.add_argument('production_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True,
                            help='Production date missing or incorrect format')
        parser.add_argument('product_part_no', type=int, required=True, help='Product part number missing')
        parser.add_argument('quantity_produced', type=int, required=True, help='Quantity produced missing')
        args = parser.parse_args()

        logger.debug(f"Creating new production log with args: {args}")

        new_production_log = ProductionLog(
            production_date=args['production_date'],
            product_part_no=args['product_part_no'],
            quantity_produced=args['quantity_produced']
        )

        try:
            db.session.add(new_production_log)
            db.session.commit()
            logger.info(f"New production log created with ID {new_production_log.id}")
            return new_production_log, 201
        except Exception as e:
            logger.error(f"Error creating production log: {e}")
            abort(500, message="An error occurred while creating the production log")


class ProductionLogResource(Resource):
    @marshal_with(production_log_fields)
    def get(self, production_log_id):
        logger.info(f"GET /production_logs/{production_log_id} called")
        production_log = ProductionLog.query.get_or_404(production_log_id, description="Production log not found")
        logger.info(f"Found production log with ID {production_log_id}")
        return production_log, 200

    @marshal_with(production_log_fields)
    def put(self, production_log_id):
        logger.info(f"PUT /production_logs/{production_log_id} called")
        parser = reqparse.RequestParser()
        parser.add_argument('production_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
        parser.add_argument('product_part_no', type=int)
        parser.add_argument('quantity_produced', type=int)
        args = parser.parse_args()

        logger.debug(f"Updating production log {production_log_id} with args: {args}")

        production_log = ProductionLog.query.get_or_404(production_log_id, description="Production log not found")

        if args['production_date'] is not None:
            production_log.production_date = args['production_date']
        if args['product_part_no'] is not None:
            production_log.product_part_no = args['product_part_no']
        if args['quantity_produced'] is not None:
            production_log.quantity_produced = args['quantity_produced']

        try:
            db.session.commit()
            logger.info(f"Production log {production_log_id} updated")
            return production_log, 200
        except Exception as e:
            logger.error(f"Error updating production log {production_log_id}: {e}")
            abort(500, message="An error occurred while updating the production log")

    def delete(self, production_log_id):
        logger.info(f"DELETE /production_logs/{production_log_id} called")
        production_log = ProductionLog.query.get_or_404(production_log_id, description="Production log not found")
        try:
            db.session.delete(production_log)
            db.session.commit()
            logger.info(f"Production log {production_log_id} deleted")
            return {'message': 'Production log deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting production log {production_log_id}: {e}")
            abort(500, message="An error occurred while deleting the production log")
