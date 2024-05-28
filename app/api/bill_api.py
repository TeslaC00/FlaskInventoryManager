from flask import request
from flask_restful import Resource, reqparse, fields, marshal_with
from datetime import datetime
from sqlalchemy import text
from app.extensions import db
from app.models import Bill
from app.logger import logger

# Define output fields for marshalling
bill_fields = {
    'id': fields.Integer,
    'buyer_id': fields.Integer,
    'total_price': fields.Float,
    'date': fields.DateTime(dt_format='iso8601'),
    'purchase_order': fields.String,
    'remarks': fields.String
}


# TODO: add date automatically or manually?

# filter - buyer_id, purchase_order, date(start,end), total_price(min,max)
# sort - buyer_id, date(default), total_price

class BillListResource(Resource):
    @marshal_with(bill_fields)
    def get(self):
        logger.info('GET /bills called')

        # for filtering
        buyer_id = request.args.get('buyer_id')
        purchase_order = request.args.get('purchase_order')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_total_price = request.args.get('min_total_price')
        max_total_price = request.args.get('max_total_price')

        # for sorting
        sort_by = request.args.get('sort_by', 'date')
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)

        logger.debug(f"Filtering with buyer_id={buyer_id}, purchase_order={purchase_order}, start_date={start_date}, "
                     f"end_date={end_date}, min_total_price={min_total_price}, max_total_price={max_total_price}, ")
        logger.debug(f"Sorting by {sort_by}, limit={limit}, offset={offset}")

        query = Bill.query
        if buyer_id:
            query = query.filter_by(buyer_id=buyer_id)
        if purchase_order:
            query = query.filter_by(purchase_order=purchase_order)
        if start_date:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Bill.date >= start_date_obj)
        if end_date:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Bill.date <= end_date_obj)
        if min_total_price:
            query = query.filter(Bill.total_price >= float(min_total_price))
        if max_total_price:
            query = query.filter(Bill.total_price <= float(max_total_price))

        query.order_by(text(sort_by)).limit(limit).offset(offset)

        bills = query.all()
        logger.info(f"Found {len(bills)} bills")
        return bills, 200

    @marshal_with(bill_fields)
    def post(self):
        logger.info('POST /bills called')
        parser = reqparse.RequestParser()
        parser.add_argument('buyer_id', type=int, required=True, hint='Buyer ID missing')
        parser.add_argument('total_price', type=float, required=True, hint='Total price missing')
        parser.add_argument('date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True,
                            help='Date missing')
        parser.add_argument('purchase_order', type=str, required=True, help='Purchase order missing')
        parser.add_argument('remarks', type=str, required=False, help='Remarks missing')
        args = parser.parse_args()

        logger.debug(f"Creating new bill with args: {args}")

        try:
            new_bill = Bill(
                buyer_id=args['buyer_id'],
                total_price=args['total_price'],
                date=args['date'],
                purchase_order=args['purchase_order'],
                remarks=args['remarks']
            )
            db.session.add(new_bill)
            db.session.commit()
            logger.info(f"New bill created with ID {new_bill.id}")
            return new_bill, 201
        except Exception as e:
            logger.error(f"Error creating bill: {e}")
            return {"message": "An error occurred while creating the bill"}, 500


class BillResource(Resource):
    '''get(self, id=None): Fetches either a specific bill by id or 10 bills if no id is provided.
post(self): Adds a new bill entry to the database. Ensures the date is in the correct format.
put(self, id): Updates an existing bill by id. Checks each argument and updates if provided.
delete(self, id): Deletes a bill by id.'''

    @marshal_with(bill_fields)
    def get(self, bill_id):
        logger.info(f"GET /bills/{bill_id} called")
        bill = Bill.query.get_or_404(bill_id)
        logger.info(f"Found bill with ID {bill_id}")
        return bill, 200

    @marshal_with(bill_fields)
    def put(self, bill_id):
        logger.info(f"PUT /bills/{bill_id} called")
        parser = reqparse.RequestParser()
        parser.add_argument('buyer_id', type=int)
        parser.add_argument('total_price', type=float)
        parser.add_argument('date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
        parser.add_argument('purchase_order', type=str)
        parser.add_argument('remarks', type=str)
        args = parser.parse_args()

        logger.debug(f"Updating bill {bill_id} with args: {args}")

        bill = Bill.query.get_or_404(bill_id)

        if args['buyer_id']:
            bill.buyer_id = args['buyer_id']
        if args['total_price']:
            bill.total_price = args['total_price']
        if args['date']:
            bill.date = args['date']
        if args['purchase_order']:
            bill.purchase_order = args['purchase_order']
        if args['remarks']:
            bill.remarks = args['remarks']

        try:
            db.session.commit()
            logger.info(f"Bill {bill_id} updated")
            return bill, 200
        except Exception as e:
            logger.error(f"Error updating bill {bill_id}: {e}")
            return {"message": "An error occurred while updating the bill"}, 500

    def delete(self, bill_id):
        logger.info(f"DELETE /bills/{bill_id} called")
        bill = Bill.query.get_or_404(bill_id)
        try:
            db.session.delete(bill)
            db.session.commit()
            logger.info(f"Bill {bill_id} deleted")
            return {'message': 'Bill deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting bill {bill_id}: {e}")
            return {"message": "An error occurred while deleting the bill"}, 500
