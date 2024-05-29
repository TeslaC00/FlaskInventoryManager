from flask import request
from flask_restful import Resource, reqparse, fields, marshal_with
from sqlalchemy import text
from app.extensions import db
from app.models import Buyer
from app.logger import logger

# Define output fields for marshalling
buyer_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'GST_No': fields.String,
    'state_code': fields.Integer,
    'state_name': fields.String,
    'address': fields.String
}


# filter - name, state_code, state_name
# sort - name, state_code, state_name


class BuyerListResource(Resource):
    @marshal_with(buyer_fields)
    def get(self):
        logger.info("GET /buyers called")

        # for filtering
        name = request.args.get('name')
        state_code = request.args.get('state_code')
        state_name = request.args.get('state_name')

        # for sorting
        sort_by = request.args.get('sort_by', 'name')
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)

        logger.debug(f"Filtering with name={name}, state_code={state_code}, state_name={state_name}")
        logger.debug(f"Sorting by {sort_by}, limit={limit}, offset={offset}")

        query = Buyer.query

        if name:
            query = query.filter(Buyer.name.like(f"%{name}%"))
        if state_code:
            query = query.filter_by(state_code=state_code)
        if state_name:
            query = query.filter(Buyer.state_name.like(f"%{state_name}%"))

        buyers = query.order_by(text(sort_by)).offset(offset).limit(limit).all()
        logger.info(f"Found {len(buyers)} buyers")
        return buyers, 200

    @marshal_with(buyer_fields)
    # TODO: check if fails
    def post(self):
        logger.info("POST /buyers called")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('GST_No', type=str, required=True, help='GST No is required')
        parser.add_argument('state_code', type=int, required=True, help='State code is required')
        parser.add_argument('state_name', type=str, required=True, help='State name is required')
        parser.add_argument('address', type=str, required=True, help='Address is required')
        args = parser.parse_args()

        logger.debug(f"Creating new buyer with args: {args}")

        try:
            new_buyer = Buyer(
                name=args['name'],
                GST_No=args['GST_No'],
                state_code=args['state_code'],
                state_name=args['state_name'],
                address=args['address']
            )
            db.session.add(new_buyer)
            db.session.commit()
            logger.info(f"New buyer created with ID {new_buyer.id}")
            return new_buyer, 201
        except Exception as e:
            logger.error(f"Error creating buyer: {e}")
            return {"message": "An error occurred while creating the buyer"}, 500


class BuyerResource(Resource):
    @marshal_with(buyer_fields)
    def get(self, buyer_id):
        logger.info(f"GET /buyers/{buyer_id} called")
        buyer = Buyer.query.get_or_404(buyer_id)
        logger.info(f"Found buyer with ID {buyer_id}")
        return buyer, 200

    @marshal_with(buyer_fields)
    def put(self, buyer_id):
        logger.info(f"PUT /buyers/{buyer_id} called")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('GST_No', type=str)
        parser.add_argument('state_code', type=int)
        parser.add_argument('state_name', type=str)
        parser.add_argument('address', type=str)
        args = parser.parse_args()

        logger.debug(f"Updating buyer {buyer_id} with args: {args}")

        buyer = Buyer.query.get_or_404(buyer_id)

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

        try:
            db.session.commit()
            logger.info(f"Buyer {buyer_id} updated")
            return buyer, 200
        except Exception as e:
            logger.error(f"Error updating buyer {buyer_id}: {e}")
            return {"message": "An error occurred while updating the buyer"}, 500

    def delete(self, buyer_id):
        logger.info(f"DELETE /buyers/{buyer_id} called")
        buyer = Buyer.query.get_or_404(buyer_id)
        try:
            db.session.delete(buyer)
            db.session.commit()
            logger.info(f"Buyer {buyer_id} deleted")
            return {'message': 'Buyer deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting buyer {buyer_id}: {e}")
            return {"message": "An error occurred while deleting the buyer"}, 500
