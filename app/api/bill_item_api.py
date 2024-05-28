from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.extensions import db
from app.models import BillItem

# Define output fields for marshalling
bill_item_fields = {
    'id': fields.Integer,
    'quantity': fields.Integer,
    'price': fields.Float,
    'c_gst': fields.Float,
    's_gst': fields.Float,
    'i_gst': fields.Float,
    'bill_id': fields.Integer,
    'product_part_no': fields.Integer
}


def abort_if_bill_item_not_found(item_id):
    bill_item = BillItem.query.get(item_id)
    if not bill_item:
        abort(404, message="Bill item not found")
    return bill_item


class BillItemResource(Resource):
    @marshal_with(bill_item_fields)
    def get(self, id=None, bill_id=None):
        if id:
            item = abort_if_bill_item_not_found(id)
            return item, 200
        elif bill_id:
            items = BillItem.query.filter_by(bill_id=bill_id).all()
            return items, 200
        else:
            abort(400, message="Please provide either item id or bill id")

    @marshal_with(bill_item_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
        parser.add_argument('price', type=float, required=True, help='Price is required')
        parser.add_argument('c_gst', type=float, required=True, help='C GST is required')
        parser.add_argument('s_gst', type=float, required=True, help='S GST is required')
        parser.add_argument('i_gst', type=float, required=True, help='I GST is required')
        parser.add_argument('bill_id', type=int, required=True, help='Bill ID is required')
        parser.add_argument('product_part_no', type=int, required=True, help='Product part number is required')
        args = parser.parse_args()

        new_item = BillItem(
            quantity=args['quantity'],
            price=args['price'],
            c_gst=args['c_gst'],
            s_gst=args['s_gst'],
            i_gst=args['i_gst'],
            bill_id=args['bill_id'],
            product_part_no=args['product_part_no']
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item, 201

    @marshal_with(bill_item_fields)
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=int)
        parser.add_argument('price', type=float)
        parser.add_argument('c_gst', type=float)
        parser.add_argument('s_gst', type=float)
        parser.add_argument('i_gst', type=float)
        parser.add_argument('bill_id', type=int)
        parser.add_argument('product_part_no', type=int)
        args = parser.parse_args()

        item = abort_if_bill_item_not_found(id)

        if args['quantity']:
            item.quantity = args['quantity']
        if args['price']:
            item.price = args['price']
        if args['c_gst']:
            item.c_gst = args['c_gst']
        if args['s_gst']:
            item.s_gst = args['s_gst']
        if args['i_gst']:
            item.i_gst = args['i_gst']
        if args['bill_id']:
            item.bill_id = args['bill_id']
        if args['product_part_no']:
            item.product_part_no = args['product_part_no']

        db.session.commit()
        return item, 200

    def delete(self, id):
        item = abort_if_bill_item_not_found(id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Bill item deleted'}, 200
# TODO: add resources in init file
# api.add_resource(BillItemResource, '/bill_items', '/bill_items/<int:id>')
