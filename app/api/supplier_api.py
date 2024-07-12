from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.schemas.person_schema import PersonCreateSchema, PersonFilterSchema, PersonUpdateSchema, PersonResponseSchema
from app.services.supplier_service import SupplierService

supplier_bp = Blueprint('supplier_bp', __name__)


@supplier_bp.route('/supplier')
class SupplierListResource(MethodView):
    @supplier_bp.response(200, PersonResponseSchema(many=True))
    @supplier_bp.arguments(PersonFilterSchema, location='query')
    @supplier_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info("GET /suppliers called")
        logger.debug(f"Query Arguments={filters}")
        try:
            suppliers = SupplierService.get_all_suppliers(pagination_parameters.page, pagination_parameters.page_size,
                                                          **filters)
            pagination_parameters.item_count = suppliers.total
            logger.info(f"Found {pagination_parameters.item_count} suppliers")
            logger.debug(f"Returned suppliers: {suppliers}")
            return suppliers
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e, message=str(e))

    @supplier_bp.response(201, PersonResponseSchema)
    @supplier_bp.arguments(PersonCreateSchema)
    def post(self, data):
        logger.info("POST /supplier called")
        logger.debug(f"Creating new supplier with args: {data}")

        try:
            supplier = SupplierService.add_supplier(**data)
            logger.info(f"New Supplier created with ID {supplier.id}")
            return supplier
        except ValueError as ve:
            logger.error(f"Error creating supplier: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating supplier: {e}")
            abort(500, e)


@supplier_bp.route('/supplier/<int:supplier_id>')
class SupplierResource(MethodView):
    @supplier_bp.response(200, PersonResponseSchema)
    def get(self, supplier_id):
        logger.info(f"GET /suppliers/{supplier_id} called")
        try:
            supplier = SupplierService.get_supplier_by_id(supplier_id)
            logger.info(f"Found supplier with ID {supplier_id}")
            return supplier
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @supplier_bp.response(200, PersonResponseSchema)
    @supplier_bp.arguments(PersonUpdateSchema)
    def put(self, data, supplier_id):
        logger.info(f"PUT /suppliers/{supplier_id} called")
        logger.debug(f"Updating supplier {supplier_id} with args: {data}")

        try:
            supplier = SupplierService.update_supplier(supplier_id, data)
            logger.info(f"Supplier {supplier_id} updated")
            return supplier
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating Supplier {supplier_id}: {e}")
            abort(500, e)

    @supplier_bp.response(204)
    def delete(self, supplier_id):
        logger.info(f"DELETE /suppliers/{supplier_id} called")
        try:
            SupplierService.delete_supplier(supplier_id)
            logger.info(f"Supplier {supplier_id} deleted")
            return {'message': 'Supplier deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting supplier {supplier_id}: {e}")
            abort(500, e)
