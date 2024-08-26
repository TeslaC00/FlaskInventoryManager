from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.services.product_scrap_service import ProductScrapService
from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.schemas.product_scrap_schema import ProductScrapSchema, ProductScrapQuerySchema, ProductScrapUpdateSchema

product_scrap_bp = Blueprint('product_scrap_bp', __name__)


@product_scrap_bp.route('/product_scrap/')
class ProductScrapListResource(MethodView):
    @product_scrap_bp.response(200, ProductScrapSchema(many=True))
    @product_scrap_bp.arguments(ProductScrapQuerySchema, location='query')
    @product_scrap_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /product_scraps called')
        logger.debug(f"Query Arguments={filters}")
        try:
            product_scrap = ProductScrapService.get_all_product_scraps(pagination_parameters.page,
                                                                       pagination_parameters.page_size,
                                                                       **filters)
            pagination_parameters.item_count = product_scrap.total
            logger.info(f"Found {pagination_parameters.item_count} product_scrap")
            logger.debug(f"Returned products: {product_scrap}")
            return product_scrap
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @product_scrap_bp.response(201, ProductScrapSchema)
    @product_scrap_bp.arguments(ProductScrapSchema)
    def post(self, data):
        logger.info('POST /product_scrap called')
        logger.debug(f"Creating new product scrap with args: {data}")

        try:
            product_scrap = ProductScrapService.add_product_scrap(**data)
            logger.info(f"New product_scrap created with part_no {product_scrap.part_no}")
            return product_scrap
        except ValueError as ve:
            logger.error(f"Error creating Product: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating Product: {e}")
            abort(500, e)


@product_scrap_bp.route('/product_scrap/<int:product_part_no>/<date:date>')
class ProductScrapResource(MethodView):
    @product_scrap_bp.response(200, ProductScrapSchema)
    def get(self, product_scrap_id):
        logger.info(f"GET /product_scraps/{product_scrap_id} called")
        try:
            product_scrap = ProductScrapService.get_product_scrap_by_id(product_scrap_id)
            logger.info(f"Found product_scrap with part_no {product_scrap_id}")
            return product_scrap
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @product_scrap_bp.response(200, ProductScrapSchema)
    @product_scrap_bp.arguments(ProductScrapUpdateSchema)
    def put(self, data, product_scrap_id):
        logger.info(f"PUT /product_scraps/{product_scrap_id} called")
        logger.debug(f"Updating product scrap {product_scrap_id} with args: {data}")

        try:
            product_scrap = ProductScrapService.update_product_scrap(product_scrap_id, data)
            logger.info(f"Product {product_scrap_id} updated")
            return product_scrap
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating Product {product_scrap_id}: {e}")
            abort(500, e)

    @product_scrap_bp.response(204)
    def delete(self, product_scrap_id):
        logger.info(f"DELETE /product_scraps/{product_scrap_id} called")
        try:
            ProductScrapService.delete_product_scrap(product_scrap_id)
            logger.info(f"Product {product_scrap_id} deleted")
            return {'message': 'Product deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting Product {product_scrap_id}: {e}")
            abort(500, e)
