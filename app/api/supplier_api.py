from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app.api.utils import apply_sorting, generate_meta
from app.extensions import db
from app.logger import logger
from app.models import Supplier
from app.schemas.person_schema import PersonSchema, PersonQuerySchema, PersonUpdateSchema

supplier_bp = Blueprint('supplier_bp', __name__)


@supplier_bp.route('/supplier')
class SupplierListResource(MethodView):
    @supplier_bp.response(200, PersonSchema(many=True))
    @supplier_bp.arguments(PersonQuerySchema, location='query')
    def get(self, query_args):
        logger.info("GET /suppliers called")
        logger.debug(f"Query Arguments={query_args}")

        query = Supplier.query
        # for filtering
        if 'name' in query_args:
            query = query.filter(Supplier.name.like(f"%{query_args['name']}%"))
        if 'GST_No' in query_args:
            query = query.filter(Supplier.GST_No.like(f"%{query_args['GST_No']}%"))
        if 'state_code' in query_args:
            query = query.filter(Supplier.state_code.like(f"%{query_args['state_code']}%"))
        if 'state_name' in query_args:
            query = query.filter(Supplier.state_name.like(f"%{query_args['state_name']}%"))
        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                Supplier.name.like(search),
                Supplier.GST_No.like(search),
                Supplier.state_name.like(search),
                Supplier.address.like(search)
            ))
        # for sorting
        suppliers, records_count = apply_sorting(query, query_args)
        logger.info(f"Found {records_count} suppliers")
        logger.debug(f"Returned suppliers: {suppliers}")

        meta = generate_meta(records_count, query_args)
        return suppliers, {'meta': meta}

    @supplier_bp.response(201, PersonSchema)
    @supplier_bp.arguments(PersonSchema)
    def post(self, new_supplier_data):
        logger.info("POST /buyers called")
        logger.debug(f"Creating new supplier with args: {new_supplier_data}")

        try:
            new_supplier = Supplier(new_supplier_data)
            db.session.add(new_supplier)
            db.session.commit()
            logger.info(f"New supplier created with ID {new_supplier.id}")
            return new_supplier
        except Exception as e:
            logger.error(f"Error creating supplier: {e}")
            abort(500, message="An error occurred while creating the supplier")


@supplier_bp.route('/supplier/<int:supplier_id>')
class SupplierResource(MethodView):
    @supplier_bp.response(200, PersonSchema)
    def get(self, supplier_id):
        logger.info(f"GET /suppliers/{supplier_id} called")
        supplier = Supplier.query.get_or_404(supplier_id)
        logger.info(f"Found supplier with ID {supplier_id}")
        return supplier

    @supplier_bp.response(200, PersonSchema)
    @supplier_bp.arguments(PersonUpdateSchema)
    def put(self, update_supplier_data, supplier_id):
        logger.info(f"PUT /suppliers/{supplier_id} called")
        logger.debug(f"Updating supplier {supplier_id} with args: {update_supplier_data}")

        supplier = Supplier.query.get_or_404(supplier_id)

        for key, value in update_supplier_data.items():
            setattr(supplier, key, value)

        try:
            db.session.commit()
            logger.info(f"Supplier {supplier_id} updated")
            return supplier
        except Exception as e:
            logger.error(f"Error updating supplier {supplier_id}: {e}")
            abort(500, message="An error occurred while updating the supplier")

    @supplier_bp.response(204)
    def delete(self, supplier_id):
        logger.info(f"DELETE /suppliers/{supplier_id} called")
        supplier = Supplier.query.get_or_404(supplier_id)
        try:
            db.session.delete(supplier)
            db.session.commit()
            logger.info(f"Supplier {supplier_id} deleted")
            return {'message': 'Supplier deleted'}
        except Exception as e:
            logger.error(f"Error deleting supplier {supplier_id}: {e}")
            abort(500, message="An error occurred while deleting the supplier")
