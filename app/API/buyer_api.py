from app import create_app
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

from app.extensions import db
from app.models import Buyer

# Define output fields for marshalling
buyer_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'GST_No': fields.String,
    'state_code': fields.Integer,
    'state_name': fields.String,
    'address': fields.String
}

api = Api(create_app())


def abort_if_buyer_not_found(buyer_id):
    buyer = Buyer.query.get(buyer_id)
    if not buyer:
        abort(404, message="Buyer not found")
    return buyer


class BuyerResource(Resource):
    @marshal_with(buyer_fields)
    def get(self, id=None):
        if id:
            buyer = abort_if_buyer_not_found(id)
            return buyer, 200
        buyers = Buyer.query.all()
        return buyers, 200

    @marshal_with(buyer_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('GST_No', type=str, required=True, help='GST No is required')
        parser.add_argument('state_code', type=int, required=True, help='State code is required')
        parser.add_argument('state_name', type=str, required=True, help='State name is required')
        parser.add_argument('address', type=str, required=True, help='Address is required')
        args = parser.parse_args()

        new_buyer = Buyer(
            name=args['name'],
            GST_No=args['GST_No'],
            state_code=args['state_code'],
            state_name=args['state_name'],
            address=args['address']
        )
        db.session.add(new_buyer)
        db.session.commit()
        return new_buyer, 201

    @marshal_with(buyer_fields)
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('GST_No', type=str)
        parser.add_argument('state_code', type=int)
        parser.add_argument('state_name', type=str)
        parser.add_argument('address', type=str)
        args = parser.parse_args()

        buyer = abort_if_buyer_not_found(id)

        if args['name']:
            buyer.name = args['name']
        if args['GST_No']:
            buyer.GST_No = args['GST_No']
        if args['state_code']:
            buyer.state_code = args['state_code']
        if args['state_name']:
            buyer.state_name = args['state_name']
        if args['address']:
            buyer.address = args['address']

        db.session.commit()
        return buyer, 200

    def delete(self, id):
        buyer = abort_if_buyer_not_found(id)
        db.session.delete(buyer)
        db.session.commit()
        return {'message': 'Buyer deleted'}, 200


api.add_resource(BuyerResource, '/buyers', '/buyers/<int:id>')
