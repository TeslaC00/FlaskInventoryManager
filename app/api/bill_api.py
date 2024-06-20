from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_, extract

from app.api.utils import apply_sorting
from app.extensions import db
from app.logger import logger
from app.models import Bill
from app.schemas.bill_schema import BillSchema, BillQuerySchema, BillUpdateSchema

bills_bp = Blueprint('bills_bp', __name__, description='Operations on bills')

# app/schemas/sales_analysis_schema.py
from marshmallow import Schema, fields


class SalesAnalysisQuerySchema(Schema):
    start_date = fields.Date(required=False)
    end_date = fields.Date(required=False)
    buyer_id = fields.String(required=False)


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


@bills_bp.route('/bills/analysis')
class SalesAnalysisResource(MethodView):

    @bills_bp.arguments(SalesAnalysisQuerySchema, location='query')
    def get(self, query_args):
        logger.info('GET /bills/analysis called')
        logger.debug(f"Query Arguments={query_args}")

        # Base query for summary statistics
        summary_query = db.session.query(
            func.sum(Bill.total_price).label('total_sales'),
            func.avg(Bill.total_price).label('average_sales'),
            func.count(Bill.id).label('total_bills')
        )

        # Base query for time-series data
        timeseries_query = db.session.query(
            extract('year', Bill.date).label('year'),
            func.sum(Bill.total_price).label('total_sales')
        )

        if 'interval' in query_args:
            interval = query_args['interval']
            if interval == 'month':
                timeseries_query = timeseries_query.add_columns(extract('month', Bill.date).label('month'))
            elif interval == 'day':
                timeseries_query = timeseries_query.add_columns(extract('month', Bill.date).label('month'),
                                                                extract('day', Bill.date).label('day'))

        if 'start_date' in query_args:
            summary_query = summary_query.filter(Bill.date >= query_args['start_date'])
            timeseries_query = timeseries_query.filter(Bill.date >= query_args['start_date'])
        if 'end_date' in query_args:
            summary_query = summary_query.filter(Bill.date <= query_args['end_date'])
            timeseries_query = timeseries_query.filter(Bill.date <= query_args['end_date'])
        if 'buyer_id' in query_args:
            summary_query = summary_query.filter(Bill.buyer_id.like(f"%{query_args['buyer_id']}%"))
            timeseries_query = timeseries_query.filter(Bill.buyer_id.like(f"%{query_args['buyer_id']}%"))

        # Group by year (and optionally month/day)
        if 'interval' in query_args:
            interval = query_args['interval']
            if interval == 'month':
                timeseries_query = timeseries_query.group_by('year', 'month').order_by('year', 'month')
            elif interval == 'day':
                timeseries_query = timeseries_query.group_by('year', 'month', 'day').order_by('year', 'month', 'day')
            else:
                timeseries_query = timeseries_query.group_by('year').order_by('year')
        else:
            timeseries_query = timeseries_query.group_by('year').order_by('year')

        summary_result = summary_query.one()
        timeseries_result = timeseries_query.all()

        # Transform time-series data for plotting
        timeseries_data = []
        for row in timeseries_result:
            data_point = {
                'year': row.year,
                'total_sales': row.total_sales
            }
            if 'interval' in query_args:
                if query_args['interval'] == 'month':
                    data_point['month'] = row.month
                elif query_args['interval'] == 'day':
                    data_point['month'] = row.month
                    data_point['day'] = row.day
            timeseries_data.append(data_point)

        logger.info(f"Sales analysis: {summary_result}, Time-series data points: {len(timeseries_data)}")
        return {
            'total_sales': summary_result.total_sales or 0,
            'average_sales': summary_result.average_sales or 0,
            'total_bills': summary_result.total_bills or 0,
            'timeseries_data': timeseries_data
        }