from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.schemas.unit_schema import UnitSchema
from app.logger import logger
from app.services.unit_service import UnitService

unit_bp = Blueprint('unit_bp', __name__)


@unit_bp.route('/unit')
class UnitListResource(MethodView):
    @unit_bp.response(200, UnitSchema(many=True))
    def get(self):
        logger.info("GET /units called")
        try:
            return UnitService.get_all_units()
        except Exception as e:
            abort(500, e, message=str(e))

    @unit_bp.response(201, UnitSchema)
    @unit_bp.arguments(UnitSchema)
    def post(self, data):
        logger.info("POST /units called")
        logger.debug(f"Creating new unit with data: {data}")

        try:
            new_unit = UnitService.add_unit(**data)
            logger.info(f"New unit created with id {new_unit.id}")
            return new_unit
        except ValueError as ve:
            logger.error(f"Error creating unit: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating unit: {e}")
            abort(500, e)


@unit_bp.route('/unit/<int:unit_id>')
class UnitResource(MethodView):
    @unit_bp.response(201, UnitSchema)
    def get(self, unit_id):
        logger.info(f"GET /units/{unit_id} called")
        try:
            unit = UnitService.get_unit_by_id(unit_id)
            logger.info(f"Found unit with unit_id {unit_id}")
            return unit
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @unit_bp.response(204)
    def delete(self, unit_id):
        logger.info(f"DELETE /unit/{unit_id} called")
        try:
            UnitService.delete_unit(unit_id)
            logger.info(f"Unit {unit_id} deleted")
            return {'message': 'Unit deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting unit {unit_id}: {e}")
            abort(500, e)
