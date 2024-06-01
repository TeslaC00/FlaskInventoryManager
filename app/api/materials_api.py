from flask_restful import fields
from sqlalchemy import text
from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from app.extensions import db
from app.models import Material
from app.logger import logger

material_fields = {
    'part_no': fields.Integer,
    'name': fields.String,
    'unit': fields.String,
    'quantity': fields.Integer
}

# filter - name, unit, quantity(min,max)
# sort - name, quantity, part_no


class MaterialListResource(Resource):
    @marshal_with(material_fields)
    def get(self):
        logger.info('GET /materials called')

        # for filtering
        name = request.args.get('name')
        unit = request.args.get('unit')
        min_quantity = request.args.get('min_quantity', type=int)
        max_quantity = request.args.get('max_quantity', type=int)

        # for sorting
        sort_by = request.args.get('sort_by', 'part_no')
        limit = request.args.get('limit', type=int, default=20)
        offset = request.args.get('offset', type=int, default=0)

        query = Material.query
        if name:
            query = query.filter(Material.name.like(f"%{name}%"))
        if unit:
            query = query.filter_by(unit=unit)
        if min_quantity:
            query = query.filter(Material.quantity >= min_quantity)
        if max_quantity:
            query = query.filter(Material.quantity <= max_quantity)

        materials = query.order_by(text(sort_by)).offset(offset).limit(limit).all()
        logger.info(f"Found {len(materials)} materials")
        return materials, 200

    @marshal_with(material_fields)
    def post(self):
        logger.info('POST /materials called')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name missing')
        parser.add_argument('unit', type=str, required=True, help='Unit missing')
        parser.add_argument('quantity', type=int, required=True, help='Quantity missing')
        args = parser.parse_args()

        logger.debug(f"Creating new material with args: {args}")

        new_material = Material(
            name=args['name'],
            unit=args['unit'],
            quantity=args['quantity']
        )

        try:
            db.session.add(new_material)
            db.session.commit()
            logger.info(f"New material created with part_no {new_material.part_no}")
            return new_material, 201
        except Exception as e:
            logger.error(f"Error creating material: {e}")
            abort(500, message="An error occurred while creating the material")


class MaterialResource(Resource):
    @marshal_with(material_fields)
    def get(self, part_no):
        logger.info(f"GET /materials/{part_no} called")
        material = Material.query.get_or_404(part_no, description="Material not found")
        logger.info(f"Found material with part_no {part_no}")
        return material, 200

    @marshal_with(material_fields)
    def put(self, part_no):
        logger.info(f"PUT /materials/{part_no} called")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('unit', type=str)
        parser.add_argument('quantity', type=int)
        args = parser.parse_args()

        logger.debug(f"Updating material {part_no} with args: {args}")

        material = Material.query.get_or_404(part_no, description="Material not found")

        if args['name']:
            material.name = args['name']
        if args['unit']:
            material.unit = args['unit']
        if args['quantity']:
            material.quantity = args['quantity']

        try:
            db.session.commit()
            logger.info(f"Material {part_no} updated")
            return material, 200
        except Exception as e:
            logger.error(f"Error updating material {part_no}: {e}")
            abort(500, message="An error occurred while updating the material")

    def delete(self, part_no):
        logger.info(f"DELETE /materials/{part_no} called")
        material = Material.query.get_or_404(part_no, description="Material not found")
        try:
            db.session.delete(material)
            db.session.commit()
            logger.info(f"Material {part_no} deleted")
            return {'message': 'Material deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting material {part_no}: {e}")
            abort(500, message="An error occurred while deleting the material")
