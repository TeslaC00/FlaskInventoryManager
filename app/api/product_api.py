from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.schemas.product_schema import ProductCreateSchema, ProductResponseSchema, ProductQuerySchema, \
    ProductUpdateSchema
from app.services.product_service import ProductService

product_bp = Blueprint('product_bp', __name__)


@product_bp.route('/product')
class ProductListResource(MethodView):
    @product_bp.response(200, ProductResponseSchema(many=True))
    @product_bp.arguments(ProductQuerySchema, location='query')
    @product_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /products called')
        logger.debug(f"Query Arguments={filters}")
        try:
            products = ProductService.get_all_products(pagination_parameters.page, pagination_parameters.page_size,
                                                       **filters)
            pagination_parameters.item_count = products.total
            logger.info(f"Found {pagination_parameters.item_count} Products")
            logger.debug(f"Returned Products: {products}")
            return products
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @product_bp.response(201, ProductResponseSchema)
    @product_bp.arguments(ProductCreateSchema)
    def post(self, data):
        logger.info('POST /products called')
        logger.debug(f"Creating new product with args: {data}")

        try:
            product = ProductService.add_product(**data)
            logger.info(f"New Buyer created with ID {product.part_no}")
            return product
        except ValueError as ve:
            logger.error(f"Error creating Product: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating Product: {e}")
            abort(500, e)


@product_bp.route('/product/<int:part_no>')
class ProductResource(MethodView):
    @product_bp.response(200, ProductResponseSchema)
    def get(self, part_no):
        logger.info(f"GET /products/{part_no} called")
        try:
            product = ProductService.get_product_by_id(part_no)
            logger.info(f"Found product with part_no {part_no}")
            return product
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @product_bp.response(200, ProductResponseSchema)
    @product_bp.arguments(ProductUpdateSchema)
    def put(self, data, part_no):
        logger.info(f"PUT /products/{part_no} called")
        logger.debug(f"Updating product {part_no} with args: {data}")

        try:
            product = ProductService.update_product(part_no, data)
            logger.info(f"Product {part_no} updated")
            return product
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating Product {part_no}: {e}")
            abort(500, e)

    @product_bp.response(204)
    def delete(self, part_no):
        logger.info(f"DELETE /products/{part_no} called")
        try:
            ProductService.delete_product(part_no)
            logger.info(f"Product {part_no} deleted")
            return {'message': 'Product deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting Product {part_no}: {e}")
            abort(500, e)
