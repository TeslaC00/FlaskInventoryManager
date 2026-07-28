from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app import logger
from app.errors.not_found_error import NotFoundError
from app.models import Challan
from app.schemas.challan_schema import ChallanCreateSchema, ChallanQuerySchema, ChallanUpdateSchema, \
    ChallanListResponseSchema, ChallanResponseSchema
from app.services.challan_service import ChallanService
from app.services.challan_item_service import ChallanItemService

challan_bp = Blueprint('challan_bp', __name__)


@challan_bp.route('/challans')
class ChallanResource(MethodView):
    @challan_bp.response(200, ChallanListResponseSchema(many=True))
    @challan_bp.arguments(ChallanQuerySchema, location='query')
    @challan_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /challans called')
        logger.debug(f"Query Arguments={filters}")
        try:
            challans = ChallanService.get_all_challans(pagination_parameters.page, pagination_parameters.page_size,
                                                       **filters)
            pagination_parameters.item_count = challans.total
            logger.info(f"Found {pagination_parameters.item_count} challans")
            logger.debug(f"Returned challans: {challans}")
            return challans
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @challan_bp.response(201, ChallanResponseSchema)
    @challan_bp.arguments(ChallanCreateSchema)
    def post(self, data):
        logger.info('POST /challans called')
        logger.debug(f"Creating new challan with args: {data}")
        challan_data = {
            'supplier_id': data['supplier_id'],
            'total_price': data['total_price'],
            'date': data['date'],
            'challan_no': data['challan_no'],
            'remarks': data['remarks']
        }
        try:
            challan = ChallanService.add_challan(**challan_data)
            for item in data['items']:
                ChallanItemService.add_challan_item(challan_id=challan.id, **item)

            logger.info(f"New challan created with ID {challan.id}")
            return ChallanService.update_total_price(challan.id)
        except ValueError as ve:
            logger.error(f"Error creating challan: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating challan: {e}")
            abort(500, e)


@challan_bp.route('/challans/<int:challan_id>')
class ChallanResource(MethodView):
    @challan_bp.response(200, ChallanResponseSchema)
    def get(self, challan_id):
        logger.info(f"GET /challans/{challan_id} called")
        try:
            challan = ChallanService.get_challan_by_id(challan_id)
            logger.info(f"Found challan with ID {challan_id}")
            return challan
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @challan_bp.response(200, ChallanResponseSchema)
    @challan_bp.arguments(ChallanUpdateSchema)
    def put(self, data, challan_id):
        logger.info(f"PUT /challans/{challan_id} called")
        logger.debug(f"Updating challan {challan_id} with args: {data}")

        try:
            challan = ChallanService.update_challan(challan_id, data)
            logger.info(f"Challan {challan_id} updated")
            return challan
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating challan {challan_id}: {e}")
            abort(500, e)

    @challan_bp.response(204)
    def delete(self, challan_id):
        logger.info(f"DELETE /challans/{challan_id} called")
        try:
            ChallanService.delete_challan(challan_id)
            logger.info(f"Challan {challan_id} deleted")
            return {'message': 'Challan deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting challan {challan_id}: {e}")
            abort(500, e)
