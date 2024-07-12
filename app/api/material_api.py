from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.schemas.material_schema import MaterialQuerySchema, MaterialUpdateSchema, MaterialResponseSchema, \
    MaterialCreateSchema
from app.services.material_service import MaterialService

material_bp = Blueprint('material_bp', __name__)


@material_bp.route('/material')
class MaterialListResource(MethodView):
    @material_bp.response(200, MaterialResponseSchema(many=True))
    @material_bp.arguments(MaterialQuerySchema, location='query')
    @material_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /materials called')
        logger.debug(f"Query Arguments={filters}")
        try:
            materials = MaterialService.get_all_materials(pagination_parameters.page, pagination_parameters.page_size,
                                                          **filters)
            pagination_parameters.item_count = materials.total
            logger.info(f"Found {pagination_parameters.item_count} materials")
            logger.debug(f"Returned products: {materials}")
            return materials
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @material_bp.response(201, MaterialResponseSchema)
    # location = form ?
    @material_bp.arguments(MaterialCreateSchema)
    def post(self, data):
        logger.info('POST /materials called')
        logger.debug(f"Creating new material with data: {data}")

        try:
            material = MaterialService.add_material(**data)
            logger.info(f"New material created with part_no {material.part_no}")
            return material
        except ValueError as ve:
            logger.error(f"Error creating Material: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating Material: {e}")
            abort(500, e)


@material_bp.route('/material/<int:part_no>')
class MaterialResource(MethodView):
    @material_bp.response(200, MaterialResponseSchema)
    def get(self, part_no):
        logger.info(f"GET /materials/{part_no} called")
        try:
            material = MaterialService.get_material_by_id(part_no)
            logger.info(f"Found material with part_no {part_no}")
            return material
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @material_bp.response(200, MaterialResponseSchema)
    @material_bp.arguments(MaterialUpdateSchema)
    def put(self, data, part_no):
        logger.info(f"PUT /materials/{part_no} called")
        logger.debug(f"Updating material {part_no} with args: {data}")

        try:
            material = MaterialService.update_material(part_no, data)
            logger.info(f"Material {part_no} updated")
            return material
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating Material {part_no}: {e}")
            abort(500, e)

    @material_bp.response(204)
    def delete(self, part_no):
        logger.info(f"DELETE /materials/{part_no} called")
        try:
            MaterialService.delete_material(part_no)
            logger.info(f"Material {part_no} deleted")
            return {'message': 'Material deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting Material {part_no}: {e}")
            abort(500, e)
