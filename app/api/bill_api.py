from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from sqlalchemy import extract, func

from app.errors.not_found_error import NotFoundError
from app.extensions import db
from app.logger import logger
from app.models import Bill
from app.schemas.bill_schema import BillQuerySchema, BillUpdateSchema, BillResponseSchema, BillCreateSchema, \
    BillListResponseSchema
from app.services.bill_item_service import BillItemService
from app.services.bill_service import BillService

bills_bp = Blueprint('bills_bp', __name__, description='Operations on bills')


# app/schemas/sales_analysis_schema.py
class SalesAnalysisQuerySchema(Schema):
    start_date = fields.Date(required=False)
    end_date = fields.Date(required=False)
    buyer_id = fields.String(required=False)


@bills_bp.route('/bills')
class BillListResource(MethodView):
    @bills_bp.response(200, BillListResponseSchema(many=True))
    @bills_bp.arguments(BillQuerySchema, location='query')
    @bills_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /bills called')
        logger.debug(f"Query Arguments={filters}")
        try:
            bills = BillService.get_all_bills(pagination_parameters.page, pagination_parameters.page_size, **filters)
            pagination_parameters.item_count = bills.total
            logger.info(f"Found {pagination_parameters.item_count} bills")
            logger.debug(f"Returned bills: {bills}")
            return bills
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @bills_bp.response(201, BillResponseSchema)
    @bills_bp.arguments(BillCreateSchema)
    def post(self, data):
        logger.info('POST /bills called')
        logger.debug(f"Creating new bill with args: {data}")
        bill_data = {
            'buyer_id': data['buyer_id'],
            'total_price': data['total_price'],
            'date': data['date'],
            'purchase_order': data['purchase_order'],
            'remarks': data['remarks']
        }
        try:
            bill = BillService.add_bill(**bill_data)
            for item in data['items']:
                BillItemService.add_bill_item(bill_id=bill.id, **item)

            logger.info(f"New bill created with ID {bill.id}")
            return BillService.update_total_price(bill.id)
        except ValueError as ve:
            logger.error(f"Error creating bill: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating bill: {e}")
            abort(500, e)


@bills_bp.route('bills/<int:bill_id>')
class BillResource(MethodView):

    @bills_bp.response(200, BillResponseSchema)
    def get(self, bill_id):
        logger.info(f"GET /bills/{bill_id} called")
        try:
            bill = BillService.get_bill_by_id(bill_id)
            logger.info(f"Found bill with ID {bill_id}")
            return bill
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @bills_bp.response(200, BillResponseSchema)
    @bills_bp.arguments(BillUpdateSchema)
    def put(self, data, bill_id):
        logger.info(f"PUT /bills/{bill_id} called")
        logger.debug(f"Updating bill {bill_id} with args: {data}")

        try:
            bill = BillService.update_bill(bill_id, data)
            logger.info(f"Bill {bill_id} updated")
            return bill
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating bill {bill_id}: {e}")
            abort(500, e)

    @bills_bp.response(204)
    def delete(self, bill_id):
        logger.info(f"DELETE /bills/{bill_id} called")
        try:
            BillService.delete_bill(bill_id)
            logger.info(f"Bill {bill_id} deleted")
            return {'message': 'Bill deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting bill {bill_id}: {e}")
            abort(500, e)


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
