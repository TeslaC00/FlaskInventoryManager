from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from app.extensions import db
from app.models import ChallanItem
from app.logger import logger
from flask_restful import fields

challan_item_fields = {
    'id': fields.Integer,
    'price': fields.Float,
    'quantity': fields.Integer,
    'challan_id': fields.Integer,
    'material_part_no': fields.Integer
}


class ChallanItemListResource(Resource):
    @marshal_with(challan_item_fields)
    def get(self):
        logger.info('GET /challan_items called')
        challan_items = ChallanItem.query.all()
        logger.info(f"Found {len(challan_items)} challan items")
        return challan_items, 200

    @marshal_with(challan_item_fields)
    def post(self):
        logger.info('POST /challan_items called')
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='Price is required')
        parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
        parser.add_argument('challan_id', type=int, required=True, help='Challan ID is required')
        parser.add_argument('material_part_no', type=int, required=True, help='Material part number is required')
        args = parser.parse_args()

        logger.debug(f"Creating new challan item with args: {args}")

        new_challan_item = ChallanItem(
            price=args['price'],
            quantity=args['quantity'],
            challan_id=args['challan_id'],
            material_part_no=args['material_part_no']
        )

        try:
            db.session.add(new_challan_item)
            db.session.commit()
            logger.info(f"New challan item created with ID {new_challan_item.id}")
            return new_challan_item, 201
        except Exception as e:
            logger.error(f"Error creating challan item: {e}")
            abort(500, message="An error occurred while creating the challan item")


class ChallanItemResource(Resource):
    @marshal_with(challan_item_fields)
    def get(self, id):
        logger.info(f"GET /challan_items/{id} called")
        challan_item = ChallanItem.query.get_or_404(id, description="Challan item not found")
        logger.info(f"Found challan item with ID {id}")
        return challan_item, 200

    @marshal_with(challan_item_fields)
    def put(self, id):
        logger.info(f"PUT /challan_items/{id} called")
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float)
        parser.add_argument('quantity', type=int)
        parser.add_argument('challan_id', type=int)
        parser.add_argument('material_part_no', type=int)
        args = parser.parse_args()

        logger.debug(f"Updating challan item {id} with args: {args}")

        challan_item = ChallanItem.query.get_or_404(id, description="Challan item not found")

        if args['price'] is not None:
            challan_item.price = args['price']
        if args['quantity'] is not None:
            challan_item.quantity = args['quantity']
        if args['challan_id'] is not None:
            challan_item.challan_id = args['challan_id']
        if args['material_part_no'] is not None:
            challan_item.material_part_no = args['material_part_no']

        try:
            db.session.commit()
            logger.info(f"Challan item {id} updated")
            return challan_item, 200
        except Exception as e:
            logger.error(f"Error updating challan item {id}: {e}")
            abort(500, message="An error occurred while updating the challan item")

    def delete(self, id):
        logger.info(f"DELETE /challan_items/{id} called")
        challan_item = ChallanItem.query.get_or_404(id, description="Challan item not found")
        try:
            db.session.delete(challan_item)
            db.session.commit()
            logger.info(f"Challan item {id} deleted")
            return {'message': 'Challan item deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting challan item {id}: {e}")
            abort(500, message="An error occurred while deleting the challan item")
