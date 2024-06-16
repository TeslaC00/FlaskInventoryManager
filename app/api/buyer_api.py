from flask import request
from flask_restful import Resource, fields, marshal_with
from sqlalchemy import text
from app.extensions import db
from app.models import Buyer
from app.logger import logger
from werkzeug.exceptions import BadRequest

# Define output fields for marshalling
buyer_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'GST_No': fields.String,
    'state_code': fields.Integer,
    'state_name': fields.String,
    'address': fields.String
}


class BuyerListResource(Resource):
    @marshal_with(buyer_fields)
    def get(self):
        logger.info("GET /buyers called")

        # Filtering parameters
        name = request.args.get('name')
        state_code = request.args.get('state_code')
        state_name = request.args.get('state_name')

        # Sorting and pagination parameters
        sort_by = request.args.get('sort_by', 'name')
        limit = request.args.get('limit', default=20, type=int)
        offset = request.args.get('offset', default=0, type=int)

        if sort_by not in ['name', 'state_code', 'state_name']:
            raise BadRequest(f"Invalid sort_by parameter: {sort_by}")

        logger.debug(f"Filtering with name={name}, state_code={state_code}, state_name={state_name}")
        logger.debug(f"Sorting by {sort_by}, limit={limit}, offset={offset}")

        query = Buyer.query

        if name:
            query = query.filter(Buyer.name.ilike(f"%{name}%"))
        if state_code:
            query = query.filter_by(state_code=state_code)
        if state_name:
            query = query.filter(Buyer.state_name.ilike(f"%{state_name}%"))

        buyers = query.order_by(text(sort_by)).offset(offset).limit(limit).all()
        logger.info(f"Found {len(buyers)} buyers")
        return buyers, 200

    @marshal_with(buyer_fields)
    def post(self):
        logger.info("POST /buyers called")

        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        required_fields = ['name', 'GST_No', 'state_code', 'state_name', 'address']
        for field in required_fields:
            if field not in json_data:
                return {"message": f"{field} is required"}, 400

        try:
            new_buyer = Buyer(
                name=json_data['name'],
                GST_No=json_data['GST_No'],
                state_code=json_data['state_code'],
                state_name=json_data['state_name'],
                address=json_data['address']
            )
            db.session.add(new_buyer)
            db.session.commit()
            logger.info(f"New buyer created with ID {new_buyer.id}")
            return new_buyer, 201
        except Exception as e:
            logger.error(f"Error creating buyer: {e}", exc_info=True)
            db.session.rollback()
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

        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        buyer = Buyer.query.get_or_404(buyer_id)
        for key, value in json_data.items():
            if key in ['name', 'GST_No', 'state_code', 'state_name', 'address']:
                setattr(buyer, key, value)

        try:
            db.session.commit()
            logger.info(f"Buyer {buyer_id} updated")
            return buyer, 200
        except Exception as e:
            logger.error(f"Error updating buyer {buyer_id}: {e}", exc_info=True)
            db.session.rollback()
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
            logger.error(f"Error deleting buyer {buyer_id}: {e}", exc_info=True)
            db.session.rollback()
            return {"message": "An error occurred while deleting the buyer"}, 500
