from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.schemas.product_material_schema import ProductMaterialResponseSchema, ProductMaterialSchema, \
    ProductMaterialUpdateSchema
from app.services.product_material_service import ProductMaterialService

product_material_bp = Blueprint('product_material_bp', __name__)


@product_material_bp.route('/product_material')
class ProductMaterialListResource(MethodView):

    @product_material_bp.response(200, ProductMaterialResponseSchema(many=True))
    @product_material_bp.paginate()
    def get(self, pagination_parameters):
        logger.info('GET /product_materials called')
        try:
            materials = ProductMaterialService.get_all_product_materials(pagination_parameters.page,
                                                                         pagination_parameters.page_size)
            pagination_parameters.item_count = materials.total
            logger.info(f"Found {pagination_parameters.item_count} materials")
            logger.debug(f"Returned products: {materials}")
            return materials
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @product_material_bp.response(201, ProductMaterialResponseSchema)
    @product_material_bp.arguments(ProductMaterialSchema)
    def post(self, data):
        logger.info('POST /product_materials called')
        logger.debug(f"Creating new product product_material with args: {data}")

        try:
            product_material = ProductMaterialService.add_product_material(**data)
            logger.info(f"New product_material created with part_no {product_material.part_no}")
            return product_material
        except ValueError as ve:
            logger.error(f"Error creating ProductMaterial: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating ProductMaterial: {e}")
            abort(500, e)


@product_material_bp.route('/product_material/<int:product_part_no>/<int:material_part_no>')
class ProductMaterialResource(MethodView):
    @product_material_bp.response(200, ProductMaterialResponseSchema)
    def get(self, product_part_no, material_part_no):
        logger.info(f"GET /product_materials/{product_part_no}/{material_part_no} called")
        try:
            product_material = ProductMaterialService.get_product_material_by_id(product_part_no, material_part_no)
            logger.info(f"Found product_material with part_no {product_part_no, material_part_no}")
            return product_material
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @product_material_bp.response(200, ProductMaterialResponseSchema)
    @product_material_bp.arguments(ProductMaterialUpdateSchema)
    def put(self, data, product_part_no, material_part_no):
        logger.info(f"PUT /product_materials/{product_part_no}/{material_part_no} called")
        logger.debug(
            f"Updating product product_material {product_part_no}/{material_part_no} with args: {data}")

        try:
            product_material = ProductMaterialService.update_product_material(product_part_no, material_part_no, data)
            logger.info(f"ProductMaterial {product_part_no, material_part_no} updated")
            return product_material
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating ProductMaterial {product_part_no, material_part_no}: {e}")
            abort(500, e)

    @product_material_bp.response(204)
    def delete(self, product_part_no, material_part_no):
        logger.info(f"DELETE /product_materials/{product_part_no}/{material_part_no} called")
        try:
            ProductMaterialService.delete_product_material(product_part_no, material_part_no)
            logger.info(f"ProductMaterial {product_part_no, material_part_no} deleted")
            return {'message': 'ProductMaterial deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting ProductMaterial {product_part_no, material_part_no}: {e}")
            abort(500, e)
