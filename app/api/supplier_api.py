from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from app.extensions import db
from app.models import Supplier
from app.logger import logger
from flask_restful import fields
from sqlalchemy import text

supplier_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'GST_No': fields.String,
    'state_code': fields.Integer,
    'state_name': fields.String,
    'address': fields.String
}


# filter - name, state_code, state_name
# sort - name, state_code, state_name


class SupplierListResource(Resource):
    @marshal_with(supplier_fields)
    def get(self):
        logger.info('GET /suppliers called')

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

        query = Supplier.query

        if name:
            query = query.filter(Supplier.name.like(f"%{name}%"))
        if state_code:
            query = query.filter_by(state_code=state_code)
        if state_name:
            query = query.filter(Supplier.state_name.like(f"%{state_name}%"))

        suppliers = query.order_by(text(sort_by)).offset(offset).limit(limit).all()
        logger.info(f"Found {len(suppliers)} suppliers")
        return suppliers, 200

    @marshal_with(supplier_fields)
    def post(self):
        logger.info('POST /suppliers called')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('GST_No', type=str, required=True, help='GST No is required')
        parser.add_argument('state_code', type=int, required=True, help='State code is required')
        parser.add_argument('state_name', type=str, required=True, help='State name is required')
        parser.add_argument('address', type=str, required=True, help='Address is required')
        args = parser.parse_args()

        logger.debug(f"Creating new supplier with args: {args}")

        new_supplier = Supplier(
            name=args['name'],
            GST_No=args['GST_No'],
            state_code=args['state_code'],
            state_name=args['state_name'],
            address=args['address']
        )

        try:
            db.session.add(new_supplier)
            db.session.commit()
            logger.info(f"New supplier created with ID {new_supplier.id}")
            return new_supplier, 201
        except Exception as e:
            logger.error(f"Error creating supplier: {e}")
            abort(500, message="An error occurred while creating the supplier")


class SupplierResource(Resource):
    @marshal_with(supplier_fields)
    def get(self, supplier_id):
        logger.info(f"GET /suppliers/{supplier_id} called")
        supplier = Supplier.query.get_or_404(supplier_id, description="Supplier not found")
        logger.info(f"Found supplier with ID {supplier_id}")
        return supplier, 200

    @marshal_with(supplier_fields)
    def put(self, supplier_id):
        logger.info(f"PUT /suppliers/{supplier_id} called")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('GST_No', type=str)
        parser.add_argument('state_code', type=int)
        parser.add_argument('state_name', type=str)
        parser.add_argument('address', type=str)
        args = parser.parse_args()

        logger.debug(f"Updating supplier {supplier_id} with args: {args}")

        supplier = Supplier.query.get_or_404(supplier_id, description="Supplier not found")

        if args['name']:
            supplier.name = args['name']
        if args['GST_No']:
            supplier.GST_No = args['GST_No']
        if args['state_code']:
            supplier.state_code = args['state_code']
        if args['state_name']:
            supplier.state_name = args['state_name']
        if args['address']:
            supplier.address = args['address']

        try:
            db.session.commit()
            logger.info(f"Supplier {supplier_id} updated")
            return supplier, 200
        except Exception as e:
            logger.error(f"Error updating supplier {supplier_id}: {e}")
            abort(500, message="An error occurred while updating the supplier")

    def delete(self, supplier_id):
        logger.info(f"DELETE /suppliers/{supplier_id} called")
        supplier = Supplier.query.get_or_404(supplier_id, description="Supplier not found")
        try:
            db.session.delete(supplier)
            db.session.commit()
            logger.info(f"Supplier {supplier_id} deleted")
            return {'message': 'Supplier deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting supplier {supplier_id}: {e}")
            abort(500, message="An error occurred while deleting the supplier")
