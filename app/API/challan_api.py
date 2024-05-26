from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from datetime import datetime
import app
from app.extensions import db
from app.models import Challan

# Define output fields for marshalling
challan_fields = {
    'challan_no': fields.Integer,
    'supplier_id': fields.Integer,
    'total_price': fields.Float,
    'date': fields.DateTime(dt_format='iso8601'),
    'remarks': fields.String
}

api = Api(app.create_app())


def abort_if_challan_not_found(challan_no):
    challan = Challan.query.filter_by(challan_no=challan_no).first()
    if not challan:
        abort(404, message="Challan not found")
    return challan


class ChallanResource(Resource):
    @marshal_with(challan_fields)
    def get(self, challan_no=None):
        if challan_no:
            challan = abort_if_challan_not_found(challan_no)
            return challan, 200
        else:
            abort(400, message="Please provide challan number")

    @marshal_with(challan_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('challan_no', type=int, required=True, help='Challan number is required')
        parser.add_argument('supplier_id', type=int, required=True, help='Supplier ID is required')
        parser.add_argument('total_price', type=float, required=True, help='Total price is required')
        parser.add_argument('date', type=str, required=True, help='Date is required')
        parser.add_argument('remarks', type=str)
        args = parser.parse_args()

        try:
            date = datetime.strptime(args['date'], '%Y-%m-%d')
        except ValueError:
            abort(400, message="Date must be in YYYY-MM-DD format")

        new_challan = Challan(
            challan_no=args['challan_no'],
            supplier_id=args['supplier_id'],
            total_price=args['total_price'],
            date=date,
            remarks=args.get('remarks')
        )
        db.session.add(new_challan)
        db.session.commit()
        return new_challan, 201

    @marshal_with(challan_fields)
    def put(self, challan_no):
        parser = reqparse.RequestParser()
        parser.add_argument('supplier_id', type=int)
        parser.add_argument('total_price', type=float)
        parser.add_argument('date', type=str)
        parser.add_argument('remarks', type=str)
        args = parser.parse_args()

        challan = abort_if_challan_not_found(challan_no)

        if args['supplier_id']:
            challan.supplier_id = args['supplier_id']
        if args['total_price']:
            challan.total_price = args['total_price']
        if args['date']:
            try:
                challan.date = datetime.strptime(args['date'], '%Y-%m-%d')
            except ValueError:
                abort(400, message="Date must be in YYYY-MM-DD format")
        if args['remarks']:
            challan.remarks = args['remarks']

        db.session.commit()
        return challan, 200

    def delete(self, challan_no):
        challan = abort_if_challan_not_found(challan_no)
        db.session.delete(challan)
        db.session.commit()
        return {'message': 'Challan deleted'}, 200


api.add_resource(ChallanResource, '/challans', '/challans/<int:challan_no>')
