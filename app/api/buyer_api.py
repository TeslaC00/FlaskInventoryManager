from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app.api.utils import apply_sorting
from app.extensions import db
from app.logger import logger
from app.models import Buyer
from app.schemas.person_schema import PersonCreateSchema, PersonQuerySchema, PersonUpdateSchema, PersonResponseSchema

buyer_bp = Blueprint('buyer_bp', __name__)


@buyer_bp.route('/buyer')
class BuyerListResource(MethodView):
    @buyer_bp.response(200, PersonResponseSchema(many=True))
    @buyer_bp.arguments(PersonQuerySchema, location='query')
    @buyer_bp.paginate()
    def get(self, query_args, pagination_parameters):
        logger.info("GET /buyers called")
        logger.debug(f"Query Arguments={query_args}, pagination={pagination_parameters}")

        query = Buyer.query
        # for filtering
        if 'name' in query_args:
            query = query.filter(Buyer.name.like(f"%{query_args['name']}%"))
        if 'GST_No' in query_args:
            query = query.filter(Buyer.GST_No.like(f"%{query_args['GST_No']}%"))
        if 'state_code' in query_args:
            query = query.filter(Buyer.state_code.like(f"%{query_args['state_code']}%"))
        if 'state_name' in query_args:
            query = query.filter(Buyer.state_name.like(f"%{query_args['state_name']}%"))
        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                Buyer.name.like(search),
                Buyer.GST_No.like(search),
                Buyer.state_name.like(search),
                Buyer.address.like(search)
            ))
        # for sorting
        buyers = apply_sorting(query, query_args, pagination_parameters)
        logger.info(f"Found {pagination_parameters.item_count} buyers")
        logger.debug(f"Returned buyers: {buyers}")
        return buyers

    @buyer_bp.response(201, PersonResponseSchema)
    @buyer_bp.arguments(PersonCreateSchema)
    def post(self, new_buyer_data):
        logger.info("POST /buyers called")
        logger.debug(f"Creating new buyer with args: {new_buyer_data}")

        try:
            new_buyer = Buyer(**new_buyer_data)
            db.session.add(new_buyer)
            db.session.commit()
            logger.info(f"New buyer created with ID {new_buyer.id}")
            return new_buyer
        except Exception as e:
            logger.error(f"Error creating buyer: {e}")
            abort(500, message="An error occurred while creating the buyer")


@buyer_bp.route('/buyer/<int:buyer_id>')
class BuyerResource(MethodView):
    @buyer_bp.response(200, PersonResponseSchema)
    def get(self, buyer_id):
        logger.info(f"GET /buyers/{buyer_id} called")
        buyer = Buyer.query.get_or_404(buyer_id)
        logger.info(f"Found buyer with ID {buyer_id}")
        return buyer

    @buyer_bp.response(200, PersonResponseSchema)
    @buyer_bp.arguments(PersonUpdateSchema)
    def put(self, update_buyer_data, buyer_id):
        logger.info(f"PUT /buyers/{buyer_id} called")
        logger.debug(f"Updating buyer {buyer_id} with args: {update_buyer_data}")

        buyer = Buyer.query.get_or_404(buyer_id)

        for key, value in update_buyer_data.items():
            setattr(buyer, key, value)

        try:
            db.session.commit()
            logger.info(f"Buyer {buyer_id} updated")
            return buyer
        except Exception as e:
            logger.error(f"Error updating buyer {buyer_id}: {e}")
            abort(500, message="An error occurred while updating the buyer")

    @buyer_bp.response(204)
    def delete(self, buyer_id):
        logger.info(f"DELETE /buyers/{buyer_id} called")
        buyer = Buyer.query.get_or_404(buyer_id)
        try:
            db.session.delete(buyer)
            db.session.commit()
            logger.info(f"Buyer {buyer_id} deleted")
            return {'message': 'Buyer deleted'}
        except Exception as e:
            logger.error(f"Error deleting buyer {buyer_id}: {e}")
            abort(500, message="An error occurred while deleting the buyer")
