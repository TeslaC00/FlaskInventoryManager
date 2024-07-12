from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.schemas.person_schema import PersonCreateSchema, PersonFilterSchema, PersonUpdateSchema, PersonResponseSchema
from app.services.buyer_service import BuyerService

buyer_bp = Blueprint('buyer_bp', __name__)


@buyer_bp.route('/buyer')
class BuyerListResource(MethodView):
    @buyer_bp.response(200, PersonResponseSchema(many=True))
    @buyer_bp.arguments(PersonFilterSchema, location='query')
    @buyer_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info("GET /buyers called")
        logger.debug(f"Query Arguments={filters}, pagination={pagination_parameters}")
        try:
            buyers = BuyerService.get_all_buyers(pagination_parameters.page, pagination_parameters.page_size, **filters)
            pagination_parameters.item_count = buyers.total
            logger.info(f"Found {pagination_parameters.item_count} buyers")
            logger.debug(f"Returned buyers: {buyers}")
            return buyers
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e, message=str(e))

    @buyer_bp.response(201, PersonResponseSchema)
    @buyer_bp.arguments(PersonCreateSchema)
    def post(self, data):
        logger.info("POST /buyers called")
        logger.debug(f"Creating new buyer with args: {data}")

        try:
            return BuyerService.add_buyer(**data)
        except ValueError as ve:
            logger.error(f"Error creating buyer: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating buyer: {e}")
            abort(500, e, message='Internal Server Error')


@buyer_bp.route('/buyer/<int:buyer_id>')
class BuyerResource(MethodView):
    @buyer_bp.response(200, PersonResponseSchema)
    def get(self, buyer_id):
        logger.info(f"GET /buyers/{buyer_id} called")
        try:
            buyer = BuyerService.get_buyer_by_id(buyer_id)
            logger.info(f"Found buyer with ID {buyer_id}")
            return buyer
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e, message='Internal Server Error')

    @buyer_bp.response(200, PersonResponseSchema)
    @buyer_bp.arguments(PersonUpdateSchema)
    def put(self, data, buyer_id):
        logger.info(f"PUT /buyers/{buyer_id} called")
        logger.debug(f"Updating buyer {buyer_id} with args: {data}")

        try:
            buyer = BuyerService.update_buyer(buyer_id, data)
            logger.info(f"Buyer {buyer_id} updated")
            return buyer
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating buyer {buyer_id}: {e}")
            abort(500, e, message='Internal Server Error')

    @buyer_bp.response(204)
    def delete(self, buyer_id):
        logger.info(f"DELETE /buyers/{buyer_id} called")
        try:
            BuyerService.delete_buyer(buyer_id)
            logger.info(f"Buyer {buyer_id} deleted")
            return {'message': 'Buyer deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting buyer {buyer_id}: {e}")
            abort(500, e, message='Internal Server Error')
