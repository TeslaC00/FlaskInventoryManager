from flask_restful import fields
from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from sqlalchemy import text

from app.extensions import db
from app.models import ProductMaterial
from app.logger import logger

product_material_fields = {
    'product_part_no': fields.Integer,
    'material_part_no': fields.Integer,
    'quantity': fields.Integer
}


class ProductMaterialListResource(Resource):
    @marshal_with(product_material_fields)
    def get(self):
        logger.info('GET /product_materials called')

        # for filtering
        product_part_no = request.args.get('product_part_no', type=int)
        material_part_no = request.args.get('material_part_no', type=int)

        # for sorting
        sort_by = request.args.get('sort_by', 'product_part_no')
        limit = request.args.get('limit', type=int, default=20)
        offset = request.args.get('offset', type=int, default=0)

        query = ProductMaterial.query
        if product_part_no is not None:
            query = query.filter_by(product_part_no=product_part_no)
        if material_part_no is not None:
            query = query.filter_by(material_part_no=material_part_no)

        product_materials = query.order_by(text(sort_by)).offset(offset).limit(limit).all()
        logger.info(f"Found {len(product_materials)} product materials")
        return product_materials, 200

    @marshal_with(product_material_fields)
    def post(self):
        logger.info('POST /product_materials called')
        parser = reqparse.RequestParser()
        parser.add_argument('product_part_no', type=int, required=True, help='Product part number missing')
        parser.add_argument('material_part_no', type=int, required=True, help='Material part number missing')
        parser.add_argument('quantity', type=int, required=True, help='Quantity missing')
        args = parser.parse_args()

        logger.debug(f"Creating new product material with args: {args}")

        new_product_material = ProductMaterial(
            product_part_no=args['product_part_no'],
            material_part_no=args['material_part_no'],
            quantity=args['quantity']
        )

        try:
            db.session.add(new_product_material)
            db.session.commit()
            logger.info(
                f"New product material created with product_part_no {new_product_material.product_part_no} and material_part_no {new_product_material.material_part_no}")
            return new_product_material, 201
        except Exception as e:
            logger.error(f"Error creating product material: {e}")
            abort(500, message="An error occurred while creating the product material")


class ProductMaterialResource(Resource):
    @marshal_with(product_material_fields)
    def get(self, product_part_no, material_part_no):
        logger.info(f"GET /product_materials/{product_part_no}/{material_part_no} called")
        product_material = ProductMaterial.query.filter_by(product_part_no=product_part_no,
                                                           material_part_no=material_part_no).first_or_404(
            description="Product material not found")
        logger.info(
            f"Found product material with product_part_no {product_part_no} and material_part_no {material_part_no}")
        return product_material, 200

    @marshal_with(product_material_fields)
    def put(self, product_part_no, material_part_no):
        logger.info(f"PUT /product_materials/{product_part_no}/{material_part_no} called")
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=int)
        args = parser.parse_args()

        logger.debug(f"Updating product material {product_part_no}/{material_part_no} with args: {args}")

        product_material = ProductMaterial.query.filter_by(product_part_no=product_part_no,
                                                           material_part_no=material_part_no).first_or_404(
            description="Product material not found")

        if args['quantity'] is not None:
            product_material.quantity = args['quantity']

        try:
            db.session.commit()
            logger.info(f"Product material {product_part_no}/{material_part_no} updated")
            return product_material, 200
        except Exception as e:
            logger.error(f"Error updating product material {product_part_no}/{material_part_no}: {e}")
            abort(500, message="An error occurred while updating the product material")

    def delete(self, product_part_no, material_part_no):
        logger.info(f"DELETE /product_materials/{product_part_no}/{material_part_no} called")
        product_material = ProductMaterial.query.filter_by(product_part_no=product_part_no,
                                                           material_part_no=material_part_no).first_or_404(
            description="Product material not found")
        try:
            db.session.delete(product_material)
            db.session.commit()
            logger.info(f"Product material {product_part_no}/{material_part_no} deleted")
            return {'message': 'Product material deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting product material {product_part_no}/{material_part_no}: {e}")
            abort(500, message="An error occurred while deleting the product material")
