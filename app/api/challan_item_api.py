from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app.api.utils import apply_sorting
from app.extensions import db
from app.logger import logger
from app.models import ChallanItem
from app.schemas.challan_item_schema import ChallanQuerySchema, ChallanItemUpdateSchema, ChallanItemCreateSchema, \
    ChallanItemResponseSchema

challan_item_bp = Blueprint('challan_item_bp', __name__)


@challan_item_bp.route('/challan_item')
class ChallanItemListResource(MethodView):
    @challan_item_bp.response(200, ChallanItemResponseSchema(many=True))
    @challan_item_bp.arguments(ChallanQuerySchema, location='query')
    @challan_item_bp.paginate()
    def get(self, query_args, pagination_parameters):
        logger.info('GET /challan_items called')
        logger.debug(f"Query Arguments={query_args}")

        query = ChallanItem.query
        # for filtering
        if 'challan_id' in query_args:
            query = query.filter(ChallanItem.challan_id.like(f"%{query_args['challan_id']}%"))
        if 'material_part_no' in query_args:
            query = query.filter(ChallanItem.material_part_no.like(f"%{query_args['material_part_no']}%"))
        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                ChallanItem.price.like(search),
                ChallanItem.quantity.like(search),
                ChallanItem.challan_id.like(search),
                ChallanItem.material_part_no.like(search)
            ))
        # for sorting
        challan_items = apply_sorting(query, query_args, pagination_parameters)
        logger.info(f"Found {pagination_parameters.item_count} challan_items")
        logger.debug(f"Returned challan_items: {challan_items}")
        return challan_items

    @challan_item_bp.response(201, ChallanItemResponseSchema)
    @challan_item_bp.arguments(ChallanItemCreateSchema)
    def post(self, new_challan_item_data):
        logger.info('POST /challan_items called')
        logger.debug(f"Creating new challan items with args: {new_challan_item_data}")

        try:
            new_challan_item = ChallanItem(**new_challan_item_data)
            db.session.add(new_challan_item)
            db.session.commit()
            logger.info(f"New challan item created with ID {new_challan_item.id}")
            return new_challan_item
        except Exception as e:
            logger.error(f"Error creating challan item: {e}")
            abort(500, message="An error occurred while creating the challan item")


@challan_item_bp.route('/challan_item/<int:challan_item_id>')
class ChallanItemResource(MethodView):
    @challan_item_bp.response(200, ChallanItemResponseSchema)
    def get(self, challan_item_id):
        logger.info(f"GET /challan_items/{challan_item_id} called")
        challan_item = ChallanItem.query.get_or_404(challan_item_id, description="Challan item not found")
        logger.info(f"Found challan item with ID {challan_item_id}")
        return challan_item

    @challan_item_bp.response(200, ChallanItemResponseSchema)
    @challan_item_bp.arguments(ChallanItemUpdateSchema)
    def put(self, update_challan_item_data, challan_item_id):
        logger.info(f"PUT /challan_items/{challan_item_id} called")
        logger.debug(f"Updating challan item {challan_item_id} with args: {update_challan_item_data}")

        challan_item = ChallanItem.query.get_or_404(challan_item_id, description="Challan item not found")
        for key, value in update_challan_item_data.items():
            setattr(challan_item, key, value)

        try:
            db.session.commit()
            logger.info(f"Challan item {challan_item_id} updated")
            return challan_item
        except Exception as e:
            logger.error(f"Error updating challan item {challan_item_id}: {e}")
            abort(500, message="An error occurred while updating the challan item")

    @challan_item_bp.response(204)
    def delete(self, challan_item_id):
        logger.info(f"DELETE /challan_items/{challan_item_id} called")
        challan_item = ChallanItem.query.get_or_404(challan_item_id, description="Challan item not found")
        try:
            db.session.delete(challan_item)
            db.session.commit()
            logger.info(f"Challan item {challan_item_id} deleted")
            return {'message': 'Challan item deleted'}
        except Exception as e:
            logger.error(f"Error deleting challan item {challan_item_id}: {e}")
            abort(500, message="An error occurred while deleting the challan item")
