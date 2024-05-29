from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from app.extensions import db
from app.models import MaterialScrap
from app.logger import logger
from flask_restful import fields

material_scrap_fields = {
    'material_part_no': fields.Integer,
    'date': fields.DateTime(dt_format='iso8601'),
    'scrap_type': fields.String,
    'quantity': fields.Integer
}


class MaterialScrapListResource(Resource):
    @marshal_with(material_scrap_fields)
    def get(self):
        logger.info('GET /material_scrap called')
        scraps = MaterialScrap.query.all()
        logger.info(f"Found {len(scraps)} material scraps")
        return scraps, 200

    @marshal_with(material_scrap_fields)
    def post(self):
        logger.info('POST /material_scrap called')
        parser = reqparse.RequestParser()
        parser.add_argument('material_part_no', type=int, required=True, help='Material part number is required')
        parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
        parser.add_argument('scrap_type', type=str, required=True, help='Scrap type is required')
        parser.add_argument('date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True,
                            help='Date is required')
        args = parser.parse_args()

        logger.debug(f"Creating new material scrap with args: {args}")

        new_scrap = MaterialScrap(
            material_part_no=args['material_part_no'],
            quantity=args['quantity'],
            scrap_type=args['scrap_type'],
            date=args['date']
        )

        try:
            db.session.add(new_scrap)
            db.session.commit()
            logger.info(f"New material scrap created with material_part_no {new_scrap.material_part_no}")
            return new_scrap, 201
        except Exception as e:
            logger.error(f"Error creating material scrap: {e}")
            abort(500, message="An error occurred while creating the material scrap")


class MaterialScrapResource(Resource):
    @marshal_with(material_scrap_fields)
    def get(self, date, material_part_no):
        logger.info(f"GET /material_scrap/{date}/{material_part_no} called")
        scrap = MaterialScrap.query.filter_by(date=date, material_part_no=material_part_no).first_or_404(
            description="Material scrap not found")
        logger.info(f"Found material scrap with date {date} and material_part_no {material_part_no}")
        return scrap, 200

    @marshal_with(material_scrap_fields)
    def put(self, date, material_part_no):
        logger.info(f"PUT /material_scrap/{date}/{material_part_no} called")
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=int)
        parser.add_argument('scrap_type', type=str)
        args = parser.parse_args()

        logger.debug(f"Updating material scrap {date} {material_part_no} with args: {args}")

        scrap = MaterialScrap.query.filter_by(date=date, material_part_no=material_part_no).first_or_404(
            description="Material scrap not found")

        if args['quantity']:
            scrap.quantity = args['quantity']
        if args['scrap_type']:
            scrap.scrap_type = args['scrap_type']

        try:
            db.session.commit()
            logger.info(f"Material scrap {date} {material_part_no} updated")
            return scrap, 200
        except Exception as e:
            logger.error(f"Error updating material scrap {date} {material_part_no}: {e}")
            abort(500, message="An error occurred while updating the material scrap")

    def delete(self, date, material_part_no):
        logger.info(f"DELETE /material_scrap/{date}/{material_part_no} called")
        scrap = MaterialScrap.query.filter_by(date=date, material_part_no=material_part_no).first_or_404(
            description="Material scrap not found")
        try:
            db.session.delete(scrap)
            db.session.commit()
            logger.info(f"Material scrap {date} {material_part_no} deleted")
            return {'message': 'Material scrap deleted'}, 200
        except Exception as e:
            logger.error(f"Error deleting material scrap {date} {material_part_no}: {e}")
            abort(500, message="An error occurred while deleting the material scrap")
