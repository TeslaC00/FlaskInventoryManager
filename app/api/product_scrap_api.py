from datetime import datetime

from flask_restful import fields
from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from app.extensions import db
from app.models import ProductScrap
from app.logger import logger
from sqlalchemy import text

product_scrap_fields = {
    'part_no': fields.Integer(attribute='product_part_no'),
    'date': fields.DateTime(dt_format='iso8601'),
    'quantity': fields.Integer,
    'scrap_type': fields.String(attribute=lambda x: x.scrap_type.value),
}


# filter - part_no, date(start,end), quantity(min,max), scrap_type
# sort - part_no, date, quantity

class ProductScrapListResource(Resource):
    @marshal_with(product_scrap_fields)
    def get(self):
        logger.info('GET /product_scraps called')

        # for filtering
        product_part_no = request.args.get('product_part_no', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_quantity = request.args.get('min_quantity')
        max_quantity = request.args.get('max_quantity')
        scrap_type = request.args.get('scrap_type')

        # for sorting
        sort_by = request.args.get('sort_by', 'date')
        limit = request.args.get('limit', type=int, default=20)
        offset = request.args.get('offset', type=int, default=0)

        query = ProductScrap.query
        if product_part_no:
            query = query.filter_by(product_part_no=product_part_no)
        if start_date:
            query = query.filter(ProductScrap.date >= start_date)
        if end_date:
            query = query.filter(ProductScrap.date <= end_date)
        if min_quantity:
            query = query.filter(ProductScrap.quantity >= min_quantity)
        if max_quantity:
            query = query.filter(ProductScrap.quantity <= max_quantity)
        if scrap_type:
            query = query.filter_by(scrap_type=scrap_type)

        product_scraps = query.order_by(text(sort_by)).offset(offset).limit(limit).all()
        logger.info(f"Found {len(product_scraps)} product scraps")
        return product_scraps, 200

    @marshal_with(product_scrap_fields)
    def post(self):
        logger.info('POST /product_scraps called')
        parser = reqparse.RequestParser()
        parser.add_argument('product_part_no', type=int, required=True, help='Product part number missing')
        parser.add_argument('quantity', type=int, required=True, help='Quantity missing')
        parser.add_argument('date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True,
                            help='Date missing or incorrect format')
        parser.add_argument('scrap_type', type=str, required=True, help='Scrap type missing')
        args = parser.parse_args()

        logger.debug(f"Creating new product scrap with args: {args}")

        new_product_scrap = ProductScrap(
            product_part_no=args['product_part_no'],
            quantity=args['quantity'],
            date=args['date'],
            scrap_type=args['scrap_type']
        )

        try:
            db.session.add(new_product_scrap)
            db.session.commit()
            logger.info(f"New product scrap created with product_part_no {new_product_scrap.product_part_no} and date "
                        f"{new_product_scrap.date}")
            return new_product_scrap, 201
        except Exception as e:
            logger.error(f"Error creating product scrap: {e}")
            abort(500, message="An error occurred while creating the product scrap")


class ProductScrapResource(Resource):
    @marshal_with(product_scrap_fields)
    def get(self, product_part_no, date):
        logger.info(f"GET /product_scraps/{product_part_no}/{date} called")
        product_scrap = ProductScrap.query.filter_by(product_part_no=product_part_no, date=date).first_or_404(
            description="Product scrap not found")
        logger.info(f"Found product scrap with product_part_no {product_part_no} and date {date}")
        return product_scrap, 200

    @marshal_with(product_scrap_fields)
    def put(self, product_part_no, date):
        logger.info(f"PUT /product_scraps/{product_part_no}/{date} called")
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=int)
        parser.add_argument('scrap_type', type=str)
        args = parser.parse_args()

        logger.debug(f"Updating product scrap {product_part_no}/{date} with args: {args}")

        product_scrap = ProductScrap.query.filter_by(product_part_no=product_part_no, date=date).first_or_404(
            description="Product scrap not found")

        if args['quantity']:
            product_scrap.quantity = args['quantity']
        if args['scrap_type']:
            product_scrap.scrap_type = args['scrap_type']

        try:
            db.session.commit()
            logger.info(f"Product scrap {product_part_no}/{date} updated")
            return product_scrap, 200
        except Exception as e:
            logger.error(f"Error updating product scrap {product_part_no}/{date}: {e}")
            abort(500, message="An error occurred while updating the product scrap")

    def delete(self, product_part_no, date):
        logger.info(f"DELETE /product_scraps/{product_part_no}/{date} called")
        product_scrap = ProductScrap.query.filter_by(product_part_no=product_part_no, date=date).first_or_404(
            description="Product scrap not found")
        try:
            db.session.delete(product_scrap)
            db.session.commit()
            logger.info(f"Product scrap {product_part_no}/{date} deleted")
            return {'message': 'Product scrap deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting product scrap {product_part_no}/{date}: {e}")
            abort(500, message="An error occurred while deleting the product scrap")
