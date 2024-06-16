# TODO: add date automatically or manually?

# filter - buyer_id, purchase_order, date(start,end), total_price(min,max)
# sort - buyer_id, date(default), total_price
from flask import request
from flask_restful import Resource, fields, marshal_with, abort
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


class BillListResource(Resource):
    @marshal_with(bill_fields)
    def get(self):
        logger.info('GET /bills called')

        # Extract filtering parameters
        buyer_id = request.args.get('buyer_id', type=int)
        purchase_order = request.args.get('purchase_order')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_total_price = request.args.get('min_total_price', type=float)
        max_total_price = request.args.get('max_total_price', type=float)

        # Extract sorting and pagination parameters
        sort_by = request.args.get('sort_by', 'date')
        limit = request.args.get('limit', default=20, type=int)
        offset = request.args.get('offset', default=0, type=int)

        logger.debug(f"Filtering with buyer_id={buyer_id}, purchase_order={purchase_order}, start_date={start_date}, "
                     f"end_date={end_date}, min_total_price={min_total_price}, max_total_price={max_total_price}")
        logger.debug(f"Sorting by {sort_by}, limit={limit}, offset={offset}")

        query = Bill.query
        if buyer_id:
            query = query.filter_by(buyer_id=buyer_id)
        if purchase_order:
            query = query.filter_by(purchase_order=purchase_order)
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Bill.date >= start_date_obj)
            except ValueError:
                abort(400, message="Start date must be in YYYY-MM-DD format")
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                query = query.filter(Bill.date <= end_date_obj)
            except ValueError:
                abort(400, message="End date must be in YYYY-MM-DD format")
        if min_total_price:
            query = query.filter(Bill.total_price >= min_total_price)
        if max_total_price:
            query = query.filter(Bill.total_price <= max_total_price)

        bills = query.order_by(text(sort_by)).offset(offset).limit(limit).all()
        logger.info(f"Found {len(bills)} bills")
        return bills, 200

    @marshal_with(bill_fields)
    def post(self):
        logger.info('POST /bills called')
        json_data = request.get_json(force=True)
        if not json_data:
            logger.error("No input data provided")
            return {"message": "No input data provided"}, 400

        try:
            new_bill = Bill(
                buyer_id=json_data['buyer_id'],
                total_price=json_data['total_price'],
                date=datetime.strptime(json_data['date'], '%Y-%m-%d'),
                purchase_order=json_data['purchase_order'],
                remarks=json_data.get('remarks')
            )
            db.session.add(new_bill)
            db.session.commit()
            logger.info(f"New bill created with ID {new_bill.id}")
            return new_bill, 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return {"message": f"Missing required field: {e}"}, 400
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            return {"message": "Date must be in YYYY-MM-DD format"}, 400
        except Exception as e:
            logger.error(f"Error creating bill: {e}", exc_info=True)
            db.session.rollback()
            return {"message": "An error occurred while creating the bill"}, 500


class BillResource(Resource):
    @marshal_with(bill_fields)
    def get(self, bill_id):
        logger.info(f"GET /bills/{bill_id} called")
        bill = Bill.query.get_or_404(bill_id)
        logger.info(f"Found bill with ID {bill_id}")
        return bill, 200

    @marshal_with(bill_fields)
    def put(self, bill_id):
        logger.info(f"PUT /bills/{bill_id} called")
        json_data = request.get_json(force=True)
        if not json_data:
            logger.error("No input data provided")
            return {"message": "No input data provided"}, 400

        bill = Bill.query.get_or_404(bill_id)
        try:
            if 'buyer_id' in json_data:
                bill.buyer_id = json_data['buyer_id']
            if 'total_price' in json_data:
                bill.total_price = json_data['total_price']
            if 'date' in json_data:
                bill.date = datetime.strptime(json_data['date'], '%Y-%m-%d')
            if 'purchase_order' in json_data:
                bill.purchase_order = json_data['purchase_order']
            if 'remarks' in json_data:
                bill.remarks = json_data['remarks']

            db.session.commit()
            logger.info(f"Bill {bill_id} updated")
            return bill, 200
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            return {"message": "Date must be in YYYY-MM-DD format"}, 400
        except Exception as e:
            logger.error(f"Error updating bill {bill_id}: {e}", exc_info=True)
            db.session.rollback()
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
            logger.error(f"Error deleting bill {bill_id}: {e}", exc_info=True)
            db.session.rollback()
            return {"message": "An error occurred while deleting the bill"}, 500

# resource routes are--
# api.add_resource(BillListResource, '/bills')
# api.add_resource(BillResource, '/bills/<int:bill_id>')
