from flask_restful import fields
from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from sqlalchemy import text

from app.extensions import db
from app.models import Product
from app.logger import logger

product_fields = {
    'part_no': fields.Integer,
    'name': fields.String,
    'unit': fields.String,  # Assuming UnitType can be serialized as a string
    'quantity': fields.Integer,
    'price': fields.Float,
    'c_gst': fields.Float,
    's_gst': fields.Float,
    'i_gst': fields.Float
}


class ProductListResource(Resource):
    @marshal_with(product_fields)
    def get(self):
        logger.info('GET /products called')

        # for filtering
        name = request.args.get('name')
        unit = request.args.get('unit')
        min_quantity = request.args.get('min_quantity', type=int)
        max_quantity = request.args.get('max_quantity', type=int)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)

        # for sorting
        sort_by = request.args.get('sort_by', 'part_no')
        limit = request.args.get('limit', type=int, default=20)
        offset = request.args.get('offset', type=int, default=0)

        query = Product.query
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))
        if unit:
            query = query.filter_by(unit=unit)
        if min_quantity is not None:
            query = query.filter(Product.quantity >= min_quantity)
        if max_quantity is not None:
            query = query.filter(Product.quantity <= max_quantity)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        products = query.order_by(text(sort_by)).offset(offset).limit(limit).all()
        logger.info(f"Found {len(products)} products")
        return products, 200

    @marshal_with(product_fields)
    def post(self):
        logger.info('POST /products called')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name missing')
        parser.add_argument('unit', type=str, required=True, help='Unit missing')
        parser.add_argument('quantity', type=int, required=True, help='Quantity missing')
        parser.add_argument('price', type=float, required=True, help='Price missing')
        parser.add_argument('c_gst', type=float, required=True, help='C-GST missing')
        parser.add_argument('s_gst', type=float, required=True, help='S-GST missing')
        parser.add_argument('i_gst', type=float, required=True, help='I-GST missing')
        args = parser.parse_args()

        logger.debug(f"Creating new product with args: {args}")

        new_product = Product(
            name=args['name'],
            unit=args['unit'],
            quantity=args['quantity'],
            price=args['price'],
            c_gst=args['c_gst'],
            s_gst=args['s_gst'],
            i_gst=args['i_gst']
        )

        try:
            db.session.add(new_product)
            db.session.commit()
            logger.info(f"New product created with part_no {new_product.part_no}")
            return new_product, 201
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            abort(500, message="An error occurred while creating the product")


class ProductResource(Resource):
    @marshal_with(product_fields)
    def get(self, part_no):
        logger.info(f"GET /products/{part_no} called")
        product = Product.query.get_or_404(part_no, description="Product not found")
        logger.info(f"Found product with part_no {part_no}")
        return product, 200

    @marshal_with(product_fields)
    def put(self, part_no):
        logger.info(f"PUT /products/{part_no} called")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('unit', type=str)
        parser.add_argument('quantity', type=int)
        parser.add_argument('price', type=float)
        parser.add_argument('c_gst', type=float)
        parser.add_argument('s_gst', type=float)
        parser.add_argument('i_gst', type=float)
        args = parser.parse_args()

        logger.debug(f"Updating product {part_no} with args: {args}")

        product = Product.query.get_or_404(part_no, description="Product not found")

        if args['name']:
            product.name = args['name']
        if args['unit']:
            product.unit = args['unit']
        if args['quantity'] is not None:
            product.quantity = args['quantity']
        if args['price'] is not None:
            product.price = args['price']
        if args['c_gst'] is not None:
            product.c_gst = args['c_gst']
        if args['s_gst'] is not None:
            product.s_gst = args['s_gst']
        if args['i_gst'] is not None:
            product.i_gst = args['i_gst']

        try:
            db.session.commit()
            logger.info(f"Product {part_no} updated")
            return product, 200
        except Exception as e:
            logger.error(f"Error updating product {part_no}: {e}")
            abort(500, message="An error occurred while updating the product")

    def delete(self, part_no):
        logger.info(f"DELETE /products/{part_no} called")
        product = Product.query.get_or_404(part_no, description="Product not found")
        try:
            db.session.delete(product)
            db.session.commit()
            logger.info(f"Product {part_no} deleted")
            return {'message': 'Product deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting product {part_no}: {e}")
            abort(500, message="An error occurred while deleting the product")
