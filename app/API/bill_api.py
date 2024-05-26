from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models import Bill

# Define output fields for marshalling
bill_fields = {
    'id': fields.Integer,
    'buyer_id': fields.Integer,
    'total_price': fields.Float,
    'date': fields.DateTime(dt_format='iso8601'),
    'purchase_order': fields.String,
    'remarks': fields.String
}

api = Api(create_app)


def abort_if_bill_not_found(bill_id):
    bill = Bill.query.get(bill_id)
    if not bill:
        abort(404, message="Bill not found")
    return bill


class BillResource(Resource):
    '''get(self, id=None): Fetches either a specific bill by id or 10 bills if no id is provided.
post(self): Adds a new bill entry to the database. Ensures the date is in the correct format.
put(self, id): Updates an existing bill by id. Checks each argument and updates if provided.
delete(self, id): Deletes a bill by id.'''
    @marshal_with(bill_fields)
    def get(self, id=None):
        if id:
            bill = abort_if_bill_not_found(id)
            return bill, 200
        bills = Bill.query.limit(10).all()
        return bills, 200

    @marshal_with(bill_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('buyer_id', type=int, required=True, help='Buyer ID is required')
        parser.add_argument('total_price', type=float, required=True, help='Total price is required')
        parser.add_argument('date', type=str, required=True, help='Date is required')
        parser.add_argument('purchase_order', type=str, required=True, help='Purchase order is required')
        parser.add_argument('remarks', type=str)
        args = parser.parse_args()

        try:
            date = datetime.strptime(args['date'], '%Y-%m-%d')
        except ValueError:
            abort(400, message="Date must be in YYYY-MM-DD format")

        new_bill = Bill(
            buyer_id=args['buyer_id'],
            total_price=args['total_price'],
            date=date,
            purchase_order=args['purchase_order'],
            remarks=args.get('remarks')
        )
        db.session.add(new_bill)
        db.session.commit()
        return new_bill, 201

    @marshal_with(bill_fields)
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('buyer_id', type=int)
        parser.add_argument('total_price', type=float)
        parser.add_argument('date', type=str)
        parser.add_argument('purchase_order', type=str)
        parser.add_argument('remarks', type=str)
        args = parser.parse_args()

        bill = abort_if_bill_not_found(id)

        if args['buyer_id']:
            bill.buyer_id = args['buyer_id']
        if args['total_price']:
            bill.total_price = args['total_price']
        if args['date']:
            try:
                bill.date = datetime.strptime(args['date'], '%Y-%m-%d')
            except ValueError:
                abort(400, message="Date must be in YYYY-MM-DD format")
        if args['purchase_order']:
            bill.purchase_order = args['purchase_order']
        if args['remarks']:
            bill.remarks = args['remarks']

        db.session.commit()
        return bill, 200

    def delete(self, id):
        bill = abort_if_bill_not_found(id)
        db.session.delete(bill)
        db.session.commit()
        return {'message': 'Bill deleted'}, 200


api.add_resource(BillResource, '/bills', '/bills/<int:id>')
