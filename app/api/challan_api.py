from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app import logger
from app.api.utils import apply_sorting, generate_meta
from app.extensions import db
from app.models import Challan
from app.schemas.challan_schema import ChallanSchema, ChallanQuerySchema, ChallanUpdateSchema

challan_bp = Blueprint('challan_bp', __name__)


@challan_bp.route('/challans')
class ChallanResource(MethodView):
    @challan_bp.response(200, ChallanSchema(many=True))
    @challan_bp.arguments(ChallanQuerySchema, location='query')
    def get(self, query_args):
        logger.info('GET /challans called')
        logger.debug(f"Query Arguments={query_args}")

        query = Challan.query
        # for filtering
        if 'supplier_id' in query_args:
            query = query.filter(Challan.supplier_id.like(f"%{query_args['supplier_id']}%"))
        if 'challan_no' in query_args:
            query = query.filter(Challan.challan_no.like(f"%{query_args['challan_no']}%"))
        if 'start_date' in query_args:
            query = query.filter(Challan.date >= query_args['start_date'])
        if 'end_date' in query_args:
            query = query.filter(Challan.date <= query_args['end_date'])
        if 'min_total_price' in query_args:
            query = query.filter(Challan.total_price >= query_args['min_total_price'])
        if 'max_total_price' in query_args:
            query = query.filter(Challan.total_price <= query_args['max_total_price'])
        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                Challan.challan_no.like(search),
                Challan.supplier_id.like(search),
                Challan.total_price.like(search),
                Challan.remarks.like(search)
            ))
        # for sorting
        buyers, records_count = apply_sorting(query, query_args)
        logger.info(f"Found {records_count} buyers")
        logger.debug(f"Returned buyers: {buyers}")

        meta = generate_meta(records_count, query_args)
        return buyers, {'meta': meta}

    @challan_bp.response(201, ChallanSchema)
    @challan_bp.arguments(ChallanSchema)
    def post(self, new_challan_data):
        logger.info('POST /challans called')
        logger.debug(f"Creating new challan with args: {new_challan_data}")
        try:
            new_challan = Challan(new_challan_data)
            db.session.add(new_challan)
            db.session.commit()
            return new_challan
        except Exception as e:
            logger.error(f"Error creating challan: {e}")
            abort(500, message="An error occurred while creating the challan")


@challan_bp.route('/challans/<int:challan_id>')
class ChallanResource(MethodView):
    @challan_bp.response(200, ChallanSchema)
    def get(self, challan_id):
        logger.info(f"GET /challans/{challan_id} called")
        challan = Challan.query.get_or_404(challan_id)
        logger.info(f"Found challan with ID {challan_id}")
        return challan

    @challan_bp.response(200, ChallanSchema)
    @challan_bp.arguments(ChallanUpdateSchema)
    def put(self, update_challan_data, challan_id):
        logger.info(f"PUT /challans/{challan_id} called")
        logger.debug(f"Updating challan {challan_id} with args: {update_challan_data}")

        challan = Challan.query.get_or_404(challan_id)
        for key, value in update_challan_data.items():
            setattr(challan, key, value)

        try:
            db.session.commit()
            logger.info(f"Challan {challan_id} updated")
            return challan
        except Exception as e:
            logger.error(f"Error updating challan {challan_id}: {e}")
            abort(500, message="An error occurred while updating the challan")

    @challan_bp.response(204)
    def delete(self, challan_id):
        logger.info(f"DELETE /challans/{challan_id} called")
        challan = Challan.query.get_or_404(challan_id)
        try:
            db.session.delete(challan)
            db.session.commit()
            logger.info(f"Challan {challan_id} deleted")
            return {'message': 'Challan deleted'}
        except Exception as e:
            logger.error(f"Error deleting challan {challan_id}: {e}")
            abort(500, message="An error occurred while deleting the challan")
