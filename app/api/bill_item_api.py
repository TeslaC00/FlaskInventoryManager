from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app import logger
from app.api.utils import apply_sorting
from app.extensions import db
from app.models import BillItem
from app.schemas.bill_item_schema import BillItemSchema, BillItemQuerySchema, BillItemUpdateSchema

bill_item_bp = Blueprint('bill_item_bp', __name__, description='Operations on bill items')


@bill_item_bp.route('/bill_item')
class BillItemListResource(MethodView):
    @bill_item_bp.response(200, BillItemSchema(many=True))
    @bill_item_bp.arguments(BillItemQuerySchema, location='query')
    @bill_item_bp.paginate()
    def get(self, query_args, pagination_parameters):
        logger.info('GET /bill_item called')
        logger.debug(f"Query Arguments={query_args}")

        query = BillItem.query
        # for filtering
        if 'bill_id' in query_args:
            query = query.filter(BillItem.bill_id == query_args['bill_id'])
        if 'product_part_no' in query_args:
            query = query.filter(BillItem.product_part_no == query_args['product_part_no'])
        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                BillItem.quantity.like(search),
                BillItem.price.like(search),
                BillItem.bill_id.like(search),
                BillItem.product_part_no.like(search)
            ))
        # for sorting
        bill_items = apply_sorting(query, query_args, pagination_parameters)
        logger.info(f"Found {pagination_parameters.item_count} bills")
        logger.debug(f"Returned bills: {bill_items}")
        return bill_items

    @bill_item_bp.response(201, BillItemSchema)
    @bill_item_bp.arguments(BillItemSchema)
    def post(self, new_bill_item_data):
        logger.info('POST /bill_item called')
        logger.debug(f"Creating new bill item with args: {new_bill_item_data}")
        try:
            new_bill_item = BillItem(**new_bill_item_data)
            db.session.add(new_bill_item)
            db.session.commit()
            logger.info(f"New bill item created with ID {new_bill_item.id}")
            return new_bill_item
        except Exception as e:
            logger.error(f"Error creating bill item: {e}")
            abort(500, message="An error occurred while creating the bill item")


@bill_item_bp.route('/bill_item/<int:bill_item_id>')
class BillItemResource(MethodView):
    @bill_item_bp.response(200, BillItemSchema)
    def get(self, bill_item_id):
        logger.info(f'GET /bill_item/{bill_item_id} called')
        bill_item = BillItem.query.get_or_404(bill_item_id)
        logger.info(f"Found bill with ID {bill_item}")
        return bill_item

    @bill_item_bp.response(200, BillItemSchema)
    @bill_item_bp.arguments(BillItemUpdateSchema)
    def put(self, update_bill_item_data, bill_item_id):

        logger.info(f"PUT /bill_item/{bill_item_id} called")
        logger.debug(f"Updating bill item {bill_item_id} with args: {update_bill_item_data}")

        bill_item = BillItem.query.get_or_404(bill_item_id)
        for key, value in update_bill_item_data.items():
            setattr(bill_item, key, value)

        try:
            db.session.commit()
            logger.info(f"Bill item {bill_item_id} updated")
            return bill_item
        except Exception as e:
            logger.error(f"Error updating bill item {bill_item_id}: {e}")
            abort(500, message="An error occurred while updating the bill item")

    @bill_item_bp.response(204)
    def delete(self, bill_item_id):
        logger.info(f"DELETE /bill_item/{bill_item_id} called")
        bill_item = BillItem.query.get_or_404(bill_item_id)
        try:
            db.session.delete(bill_item)
            db.session.commit()
            logger.info(f"Bill item {bill_item_id} deleted")
            return {'message': 'Bill item deleted'}
        except Exception as e:
            logger.error(f"Error deleting bill item {bill_item_id}: {e}")
            abort(500, message="An error occurred while deleting the bill item")
