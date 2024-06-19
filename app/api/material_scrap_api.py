from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app.api.utils import apply_sorting
from app.extensions import db
from app.logger import logger
from app.models import MaterialScrap
from app.schemas.material_scrap_schema import MaterialScrapSchema, MaterialScrapQuerySchema, MaterialScrapUpdateSchema

material_scrap_bp = Blueprint('material_scrap_bp', __name__)


@material_scrap_bp.route('/material_scrap')
class MaterialScrapListResource(MethodView):
    @material_scrap_bp.response(200, MaterialScrapSchema(many=True))
    @material_scrap_bp.arguments(MaterialScrapQuerySchema, location='query')
    @material_scrap_bp.paginate()
    def get(self, query_args, pagination_parameters):
        logger.info('GET /material_scrap called')
        logger.debug(f"Query Arguments={query_args}")

        query = MaterialScrap.query
        # for filtering
        if 'material_part_no' in query_args:
            query = query.filter(MaterialScrap.material_part_no.like(f"%{query_args['material_part_no']}%"))
        if 'start_date' in query_args:
            query = query.filter(MaterialScrap.date >= query_args['start_date'])
        if 'end_date' in query_args:
            query = query.filter(MaterialScrap.date <= query_args['end_date'])
        if 'min_quantity' in query_args:
            query = query.filter(MaterialScrap.quantity >= query_args['min_quantity'])
        if 'max_quantity' in query_args:
            query = query.filter(MaterialScrap.quantity <= query_args['max_quantity'])
        if 'scrap_type' in query_args:
            query = query.filter(MaterialScrap.scrap_type.like(f"%{query_args['scrap_type']}%"))
        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                MaterialScrap.material_part_no.like(search),
                MaterialScrap.scrap_type.like(search)
            ))
        # for sorting
        material_scraps = apply_sorting(query, query_args, pagination_parameters)
        logger.info(f"Found {pagination_parameters.item_count} material scraps")
        logger.debug(f"Returned material scraps: {material_scraps}")
        return material_scraps

    @material_scrap_bp.response(201, MaterialScrapSchema)
    @material_scrap_bp.arguments(MaterialScrapSchema)
    def post(self, new_material_scrap_data):
        logger.info('POST /material_scrap called')
        logger.debug(f"Creating new material scrap with args: {new_material_scrap_data}")

        try:
            new_scrap = MaterialScrap(**new_material_scrap_data)
            db.session.add(new_scrap)
            db.session.commit()
            logger.info(f"New material scrap created with material_part_no {new_scrap.material_part_no}")
            return new_scrap
        except Exception as e:
            logger.error(f"Error creating material scrap: {e}")
            abort(500, message="An error occurred while creating the material scrap")


@material_scrap_bp.route('/material_scrap/<int:material_part_no>/<date:date>')
class MaterialScrapResource(MethodView):
    @material_scrap_bp.response(200, MaterialScrapSchema)
    def get(self, material_part_no, date):
        logger.info(f"GET /material_scrap/{material_part_no}/{date} called")
        scrap = MaterialScrap.query.filter_by(date=date, material_part_no=material_part_no).first_or_404(
            description="Material scrap not found")
        logger.info(f"Found material scrap with date {date} and material_part_no {material_part_no}")
        return scrap

    @material_scrap_bp.response(200, MaterialScrapSchema)
    @material_scrap_bp.arguments(MaterialScrapUpdateSchema)
    def put(self, update_material_scrap_data, material_part_no, date):
        logger.info(f"PUT /material_scrap/{material_part_no}/{date} called")
        logger.debug(f"Updating material scrap {material_part_no}/{date} with args: {update_material_scrap_data}")

        scrap = MaterialScrap.query.filter_by(date=date, material_part_no=material_part_no).first_or_404(
            description="Material scrap not found")
        for key, value in update_material_scrap_data.items():
            setattr(scrap, key, value)
        try:
            db.session.commit()
            logger.info(f"Material scrap {material_part_no}/{date} updated")
            return scrap
        except Exception as e:
            logger.error(f"Error updating material scrap {material_part_no}/{date}: {e}")
            abort(500, message="An error occurred while updating the material scrap")

    @material_scrap_bp.response(204)
    def delete(self, material_part_no, date):
        logger.info(f"DELETE /material_scrap/{material_part_no}/{date} called")
        scrap = MaterialScrap.query.filter_by(date=date, material_part_no=material_part_no).first_or_404(
            description="Material scrap not found")
        try:
            db.session.delete(scrap)
            db.session.commit()
            logger.info(f"Material scrap {material_part_no}/{date} deleted")
            return {'message': 'Material scrap deleted'}
        except Exception as e:
            logger.error(f"Error deleting material scrap {material_part_no}/{date}: {e}")
            abort(500, message="An error occurred while deleting the material scrap")
