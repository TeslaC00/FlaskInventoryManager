from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app import logger
from app.errors.not_found_error import NotFoundError
from app.schemas.bill_item_schema import BillItemQuerySchema, BillItemUpdateSchema, BillItemResponseSchema
from app.services.bill_item_service import BillItemService

bill_item_bp = Blueprint('bill_item_bp', __name__, description='Operations on bill items')


@bill_item_bp.route('/bill_item')
class BillItemListResource(MethodView):
    @bill_item_bp.response(200, BillItemResponseSchema(many=True))
    @bill_item_bp.arguments(BillItemQuerySchema, location='query')
    @bill_item_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /bill_item called')
        logger.debug(f"Query Arguments={filters}")
        try:
            bill_items = BillItemService.get_all_bill_items(pagination_parameters.page, pagination_parameters.page_size,
                                                            **filters)
            pagination_parameters.item_count = bill_items.total
            logger.info(f"Found {pagination_parameters.item_count} BillItem")
            logger.debug(f"Returned BillItems: {bill_items}")
            return bill_items
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @bill_item_bp.response(503,
                           description="This API is Not maintained, using bills to create bill item is Recommended")
    def post(self):
        logger.info('POST /bill_item called')
        return ("This route is not going to be removed or inaccessible"
                "Use bills to create new bill items with it instead this one")


@bill_item_bp.route('/bill_item/<int:bill_item_id>')
class BillItemResource(MethodView):
    @bill_item_bp.response(200, BillItemResponseSchema)
    def get(self, bill_item_id):
        logger.info(f'GET /bill_item/{bill_item_id} called')
        try:
            bill_item = BillItemService.get_bill_item_by_id(bill_item_id)
            logger.info(f"Found BillItem with ID {bill_item_id}")
            return bill_item
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @bill_item_bp.response(200, BillItemResponseSchema)
    @bill_item_bp.arguments(BillItemUpdateSchema)
    def put(self, data, bill_item_id):

        logger.info(f"PUT /bill_item/{bill_item_id} called")
        logger.debug(f"Updating bill item {bill_item_id} with args: {data}")

        try:
            bill_item = BillItemService.update_bill_item(bill_item_id, data)
            logger.info(f"Bill item {bill_item_id} updated")
            return bill_item
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating BillItem {bill_item_id}: {e}")
            abort(500, e)

    @bill_item_bp.response(204)
    def delete(self, bill_item_id):
        logger.info(f"DELETE /bill_item/{bill_item_id} called")
        try:
            BillItemService.delete_bill_item(bill_item_id)
            logger.info(f"Bill item {bill_item_id} deleted")
            return {'message': 'Bill item deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting BillItem {bill_item_id}: {e}")
            abort(500, e)
