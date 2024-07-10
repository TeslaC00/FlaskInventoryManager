from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.api.utils import apply_sorting
from app.extensions import db
from app.logger import logger
from app.models import Product
from app.schemas.product_schema import ProductSchema, ProductQuerySchema, ProductUpdateSchema

product_bp = Blueprint('product_bp', __name__)


@product_bp.route('/product')
class ProductListResource(MethodView):
    @product_bp.response(200, ProductSchema(many=True))
    @product_bp.arguments(ProductQuerySchema, location='query')
    @product_bp.paginate()
    def get(self, query_args, pagination_parameters):
        logger.info('GET /products called')
        logger.debug(f"Query Arguments={query_args}")

        query = Product.query
        # for filtering
        if 'name' in query_args:
            query = query.filter(Product.name.like(f"%{query_args['name']}%"))
        if 'unit_id' in query_args:
            query = query.filter(Product.unit_id == query_args['unit_id'])
        if 'min_quantity' in query_args:
            query = query.filter(Product.quantity >= query_args['min_quantity'])
        if 'max_quantity' in query_args:
            query = query.filter(Product.quantity <= query_args['max_quantity'])
        if 'min_price' in query_args:
            query = query.filter(Product.price >= query_args['min_price'])
        if 'max_price' in query_args:
            query = query.filter(Product.price <= query_args['max_price'])
        if 'min_c_gst' in query_args:
            query = query.filter(Product.c_gst >= query_args['min_c_gst'])
        if 'max_c_gst' in query_args:
            query = query.filter(Product.c_gst <= query_args['max_c_gst'])
        if 'min_s_gst' in query_args:
            query = query.filter(Product.s_gst >= query_args['min_s_gst'])
        if 'max_s_gst' in query_args:
            query = query.filter(Product.s_gst <= query_args['max_s_gst'])
        if 'min_i_gst' in query_args:
            query = query.filter(Product.i_gst >= query_args['min_i_gst'])
        if 'max_i_gst' in query_args:
            query = query.filter(Product.i_gst <= query_args['max_i_gst'])
        # for searching
        if 'search' in query_args:
            query = query.filter(Product.name.like(f"%{query_args['search']}%"))
        # for sorting
        products = apply_sorting(query, query_args, pagination_parameters)
        logger.info(f"Found {pagination_parameters.item_count} products")
        logger.debug(f"Returned products: {products}")
        return products

    @product_bp.response(201, ProductSchema)
    @product_bp.arguments(ProductSchema)
    def post(self, new_product_data):
        logger.info('POST /products called')
        logger.debug(f"Creating new product with args: {new_product_data}")

        try:
            new_product = Product(**new_product_data)
            db.session.add(new_product)
            db.session.commit()
            logger.info(f"New product created with part_no {new_product.part_no}")
            return new_product
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            abort(500, message="An error occurred while creating the product")


@product_bp.route('/product/<int:part_no>')
class ProductResource(MethodView):
    @product_bp.response(200, ProductSchema)
    def get(self, part_no):
        logger.info(f"GET /products/{part_no} called")
        product = Product.query.get_or_404(part_no, description="Product not found")
        logger.info(f"Found product with part_no {part_no}")
        return product

    @product_bp.response(200, ProductSchema)
    @product_bp.arguments(ProductUpdateSchema)
    def put(self, update_product_data, part_no):
        logger.info(f"PUT /products/{part_no} called")
        logger.debug(f"Updating product {part_no} with args: {update_product_data}")

        product = Product.query.get_or_404(part_no, description="Product not found")
        for key, value in update_product_data.items():
            setattr(product, key, value)

        try:
            db.session.commit()
            logger.info(f"Product {part_no} updated")
            return product
        except Exception as e:
            logger.error(f"Error updating product {part_no}: {e}")
            abort(500, message="An error occurred while updating the product")

    @product_bp.response(204)
    def delete(self, part_no):
        logger.info(f"DELETE /products/{part_no} called")
        product = Product.query.get_or_404(part_no, description="Product not found")
        try:
            db.session.delete(product)
            db.session.commit()
            logger.info(f"Product {part_no} deleted")
            return {'message': 'Product deleted'}
        except Exception as e:
            logger.error(f"Error deleting product {part_no}: {e}")
            abort(500, message="An error occurred while deleting the product")
