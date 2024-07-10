from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models import Unit
from app.schemas.unit_schema import UnitSchema
from app.logger import logger
from app.extensions import db

unit_bp = Blueprint('unit_bp', __name__)


@unit_bp.route('/unit')
class UnitListResource(MethodView):
    @unit_bp.response(200, UnitSchema(many=True))
    def get(self):
        logger.info("GET /units called")
        units = Unit.query.all()
        return units

    @unit_bp.response(201, UnitSchema)
    @unit_bp.arguments(UnitSchema)
    def post(self, new_unit_data):
        logger.info("POST /units called")
        logger.debug(f"Creating new unit with data: {new_unit_data}")

        try:
            new_unit = Unit(**new_unit_data)
            db.session.add(new_unit)
            db.session.commit()
            logger.info(f"New unit created with id {new_unit.id}")
            return new_unit
        except Exception as e:
            logger.error(f"Error creating unit: {e}")
            abort(500, message="An error occurred while creating the unit")


@unit_bp.route('/unit/<int:unit_id>')
class UnitResource(MethodView):
    @unit_bp.response(201, UnitSchema)
    def get(self, unit_id):
        logger.info(f"GET /units/{unit_id} called")
        unit = Unit.query.get_or_404(unit_id, description="Material not found")
        logger.info(f"Found unit with unit_id {unit_id}")
        return unit

    @unit_bp.response(204)
    def delete(self, unit_id):
        logger.info(f"DELETE /unit/{unit_id} called")
        unit = Unit.query.get_or_404(unit_id, description="Unit not found")
        try:
            db.session.delete(unit)
            db.session.commit()
            logger.info(f"Unit {unit_id} deleted")
            return {'message': 'Unit deleted'}
        except Exception as e:
            logger.error(f"Error deleting unit {unit_id}: {e}")
            abort(500, message="An error occurred while deleting the unit")
