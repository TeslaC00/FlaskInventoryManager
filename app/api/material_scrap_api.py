from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.services.material_scrap_service import MaterialScrapService
from app.schemas.material_scrap_schema import MaterialScrapSchema, MaterialScrapQuerySchema, MaterialScrapUpdateSchema

material_scrap_bp = Blueprint('material_scrap_bp', __name__)


@material_scrap_bp.route('/material_scrap')
class MaterialScrapListResource(MethodView):
    @material_scrap_bp.response(200, MaterialScrapSchema(many=True))
    @material_scrap_bp.arguments(MaterialScrapQuerySchema, location='query')
    @material_scrap_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /material_scrap called')
        logger.debug(f"Query Arguments={filters}")
        try:
            material_scrap = MaterialScrapService.get_all_material_scraps(pagination_parameters.page,
                                                                          pagination_parameters.page_size,
                                                                          **filters)
            pagination_parameters.item_count = material_scrap.total
            logger.info(f"Found {pagination_parameters.item_count} material_scrap")
            logger.debug(f"Returned products: {material_scrap}")
            return material_scrap
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @material_scrap_bp.response(201, MaterialScrapSchema)
    @material_scrap_bp.arguments(MaterialScrapSchema)
    def post(self, data):
        logger.info('POST /material_scrap called')
        logger.debug(f"Creating new material_scrap with data: {data}")

        try:
            material_scrap = MaterialScrapService.add_material_scrap(**data)
            logger.info(f"New material_scrap created with part_no {material_scrap.part_no}")
            return material_scrap
        except ValueError as ve:
            logger.error(f"Error creating Material: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating Material: {e}")
            abort(500, e)


@material_scrap_bp.route('/material_scrap/<int:material_part_no>/<date:date>')
class MaterialScrapResource(MethodView):
    @material_scrap_bp.response(200, MaterialScrapSchema)
    def get(self, material_part_no, date):
        logger.info(f"GET /material_scrap/{material_part_no, date} called")
        try:
            material_scrap = MaterialScrapService.get_material_scrap_by_id(material_part_no, date)
            logger.info(f"Found material_scrap with part_no {material_part_no, date}")
            return material_scrap
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @material_scrap_bp.response(200, MaterialScrapSchema)
    @material_scrap_bp.arguments(MaterialScrapUpdateSchema)
    def put(self, data, material_part_no, date):
        logger.info(f"PUT /material_scrap/{material_part_no, date} called")
        logger.debug(f"Updating material_scrap {material_part_no, date} with args: {data}")

        try:
            material_scrap = MaterialScrapService.update_material_scrap(material_part_no, date, data)
            logger.info(f"Material {material_part_no, date} updated")
            return material_scrap
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating Material {material_part_no, date}: {e}")
            abort(500, e)

    @material_scrap_bp.response(204)
    def delete(self, material_part_no, date):
        logger.info(f"DELETE /material_scrap/{material_part_no, date} called")
        try:
            MaterialScrapService.delete_material_scrap(material_part_no, date)
            logger.info(f"Material {material_part_no, date} deleted")
            return {'message': 'Material deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting Material {material_part_no, date}: {e}")
            abort(500, e)
