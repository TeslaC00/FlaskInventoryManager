from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.api.utils import apply_sorting, generate_meta
from app.extensions import db
from app.logger import logger
from app.models import Material
from app.schemas.material_schema import MaterialSchema, MaterialQuerySchema, MaterialUpdateSchema

material_bp = Blueprint('material_bp', __name__)


@material_bp.route('/material')
class MaterialListResource(MethodView):
    @material_bp.response(200, MaterialSchema(many=True))
    @material_bp.arguments(MaterialQuerySchema, location='query')
    def get(self, query_args):
        logger.info('GET /materials called')
        logger.debug(f"Query Arguments={query_args}")

        query = Material.query
        # for filtering
        if 'name' in query_args:
            query = query.filter(Material.name.like(f"%{query_args['name']}%"))
        if 'unit' in query_args:
            query = query.filter(Material.unit.like(f"%{query_args['unit']}%"))
        if 'min_quantity' in query_args:
            query = query.filter(Material.quantity >= query_args['min_quantity'])
        if 'max_quantity' in query_args:
            query = query.filter(Material.quantity <= query_args['max_quantity'])
        # for searching
        if 'search' in query_args:
            query = query.filter(Material.name.like(f"%{query_args['search']}%"))
        # for sorting
        materials, records_count = apply_sorting(query, query_args)
        logger.info(f"Found {records_count} materials")
        logger.debug(f"Returned products: {materials}")

        meta = generate_meta(records_count, query_args)
        return materials, {'meta': meta}

    @material_bp.response(201, MaterialSchema)
    @material_bp.arguments(MaterialSchema)
    def post(self, new_material_data):
        logger.info('POST /materials called')
        logger.debug(f"Creating new material with args: {new_material_data}")

        try:
            new_material = Material(**new_material_data)
            db.session.add(new_material)
            db.session.commit()
            logger.info(f"New material created with part_no {new_material.part_no}")
            return new_material
        except Exception as e:
            logger.error(f"Error creating material: {e}")
            abort(500, message="An error occurred while creating the material")


@material_bp.route('/material/<int:part_no>')
class MaterialResource(MethodView):
    @material_bp.response(200, MaterialSchema)
    def get(self, part_no):
        logger.info(f"GET /materials/{part_no} called")
        material = Material.query.get_or_404(part_no, description="Material not found")
        logger.info(f"Found material with part_no {part_no}")
        return material

    @material_bp.response(200, MaterialSchema)
    @material_bp.arguments(MaterialUpdateSchema)
    def put(self, update_material_data, part_no):
        logger.info(f"PUT /materials/{part_no} called")
        logger.debug(f"Updating material {part_no} with args: {update_material_data}")

        material = Material.query.get_or_404(part_no, description="Material not found")
        for key, value in update_material_data.items():
            setattr(material, key, value)

        try:
            db.session.commit()
            logger.info(f"Material {part_no} updated")
            return material
        except Exception as e:
            logger.error(f"Error updating material {part_no}: {e}")
            abort(500, message="An error occurred while updating the material")

    @material_bp.response(204)
    def delete(self, part_no):
        logger.info(f"DELETE /materials/{part_no} called")
        material = Material.query.get_or_404(part_no, description="Material not found")
        try:
            db.session.delete(material)
            db.session.commit()
            logger.info(f"Material {part_no} deleted")
            return {'message': 'Material deleted'}
        except Exception as e:
            logger.error(f"Error deleting material {part_no}: {e}")
            abort(500, message="An error occurred while deleting the material")
