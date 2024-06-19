from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app.api.utils import apply_sorting
from app.extensions import db
from app.logger import logger
from app.models import Bill
from app.schemas.bill_schema import BillSchema, BillQuerySchema, BillUpdateSchema

bills_bp = Blueprint('bills_bp', __name__, description='Operations on bills')


@bills_bp.route('/bills')
class BillListResource(MethodView):
    @bills_bp.response(200, BillSchema(many=True))
    @bills_bp.arguments(BillQuerySchema, location='query')
    @bills_bp.paginate()
    def get(self, query_args, pagination_parameters):
        logger.info('GET /bills called')
        logger.debug(f"Query Arguments={query_args}")

        query = Bill.query
        # for filtering
        if 'buyer_id' in query_args:
            query = query.filter(Bill.buyer_id.like(f"%{query_args['buyer_id']}%"))
        if 'purchase_order' in query_args:
            query = query.filter(Bill.purchase_order.like(f"%{query_args['purchase_order']}%"))
        if 'start_date' in query_args:
            query = query.filter(Bill.date >= query_args['start_date'])
        if 'end_date' in query_args:
            query = query.filter(Bill.date <= query_args['end_date'])
        if 'min_total_price' in query_args:
            query = query.filter(Bill.total_price >= query_args['min_total_price'])
        if 'max_total_price' in query_args:
            query = query.filter(Bill.total_price <= query_args['max_total_price'])
        # for searching
        if 'search' in query_args:
            query = query.filter(or_(
                Bill.purchase_order.like(f"%{query_args['search']}%"),
                Bill.remarks.like(f"%{query_args['search']}%")
            ))
        # for sorting
        bills = apply_sorting(query, query_args, pagination_parameters)
        logger.info(f"Found {pagination_parameters.item_count} bills")
        logger.debug(f"Returned bills: {bills}")
        return bills

    @bills_bp.response(201, BillSchema)
    @bills_bp.arguments(BillSchema)
    def post(self, new_bill_data):
        logger.info('POST /bills called')
        logger.debug(f"Creating new bill with args: {new_bill_data}")

        try:
            new_bill = Bill(**new_bill_data)
            db.session.add(new_bill)
            db.session.commit()
            logger.info(f"New bill created with ID {new_bill.id}")
            return new_bill
        except Exception as e:
            logger.error(f"Error creating bill: {e}")
            abort(500, message="An error occurred while creating the bill")


@bills_bp.route('bills/<int:bill_id>')
class BillResource(MethodView):

    @bills_bp.response(200, BillSchema)
    def get(self, bill_id):
        logger.info(f"GET /bills/{bill_id} called")
        bill = Bill.query.get_or_404(bill_id)
        logger.info(f"Found bill with ID {bill_id}")
        return bill

    @bills_bp.response(200, BillSchema)
    @bills_bp.arguments(BillUpdateSchema)
    def put(self, update_bill_data, bill_id):
        logger.info(f"PUT /bills/{bill_id} called")
        logger.debug(f"Updating bill {bill_id} with args: {update_bill_data}")

        bill = Bill.query.get_or_404(bill_id)
        for key, value in update_bill_data.items():
            setattr(bill, key, value)

        try:
            db.session.commit()
            logger.info(f"Bill {bill_id} updated")
            return bill
        except Exception as e:
            logger.error(f"Error updating bill {bill_id}: {e}")
            abort(500, message="An error occurred while updating the bill")

    @bills_bp.response(204)
    def delete(self, bill_id):
        logger.info(f"DELETE /bills/{bill_id} called")
        bill = Bill.query.get_or_404(bill_id)
        try:
            db.session.delete(bill)
            db.session.commit()
            logger.info(f"Bill {bill_id} deleted")
            return {'message': 'Bill deleted'}
        except Exception as e:
            logger.error(f"Error deleting bill {bill_id}: {e}")
            abort(500, message="An error occurred while deleting the bill")
