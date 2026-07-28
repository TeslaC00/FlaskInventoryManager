from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.schemas.challan_item_schema import ChallanQuerySchema, ChallanItemUpdateSchema, ChallanItemResponseSchema
from app.services.challan_item_service import ChallanItemService

challan_item_bp = Blueprint('challan_item_bp', __name__)


@challan_item_bp.route('/challan_item')
class ChallanItemListResource(MethodView):
    @challan_item_bp.response(200, ChallanItemResponseSchema(many=True))
    @challan_item_bp.arguments(ChallanQuerySchema, location='query')
    @challan_item_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /challan_items called')
        logger.debug(f"Query Arguments={filters}")
        try:
            challan_items = ChallanItemService.get_all_challan_items(pagination_parameters.page,
                                                                     pagination_parameters.page_size,
                                                                     **filters)
            logger.info(f"Found {pagination_parameters.item_count} challan_items")
            logger.debug(f"Returned challan_items: {challan_items}")
            return challan_items
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @challan_item_bp.response(503,
                              description="This API is Not maintained, using challans to create challan item is "
                                          "Recommended")
    def post(self):
        logger.info('POST /challan_items called')
        return ("This route is not going to be removed or inaccessible"
                "Use Challans to create new challan items with it instead this one")


@challan_item_bp.route('/challan_item/<int:challan_item_id>')
class ChallanItemResource(MethodView):
    @challan_item_bp.response(200, ChallanItemResponseSchema)
    def get(self, challan_item_id):
        logger.info(f"GET /challan_items/{challan_item_id} called")
        try:
            challan_item = ChallanItemService.get_challan_item_by_id(challan_item_id)
            logger.info(f"Found challan item with ID {challan_item_id}")
            return challan_item
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @challan_item_bp.response(200, ChallanItemResponseSchema)
    @challan_item_bp.arguments(ChallanItemUpdateSchema)
    def put(self, data, challan_item_id):
        logger.info(f"PUT /challan_items/{challan_item_id} called")
        logger.debug(f"Updating challan item {challan_item_id} with args: {data}")

        try:
            challan_item = ChallanItemService.update_challan_item(challan_item_id, data)
            logger.info(f"Challan item {challan_item_id} updated")
            return challan_item
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating ChallanItem {challan_item_id}: {e}")
            abort(500, e)

    @challan_item_bp.response(204)
    def delete(self, challan_item_id):
        logger.info(f"DELETE /challan_items/{challan_item_id} called")
        try:
            ChallanItemService.delete_challan_item(challan_item_id)
            logger.info(f"Challan item {challan_item_id} deleted")
            return {'message': 'Challan item deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting ChallanItem {challan_item_id}: {e}")
            abort(500, e)
