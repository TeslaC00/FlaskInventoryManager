from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app.api.utils import apply_sorting, generate_meta
from app.extensions import db
from app.logger import logger
from app.models import ProductScrap
from app.schemas.product_scrap_schema import ProductScrapSchema, ProductScrapQuerySchema, ProductScrapUpdateSchema

product_scrap_bp = Blueprint('product_scrap_bp', __name__)


@product_scrap_bp.route('/product_scrap/')
class ProductScrapListResource(MethodView):
    @product_scrap_bp.response(200, ProductScrapSchema(many=True))
    @product_scrap_bp.arguments(ProductScrapQuerySchema, location='query')
    def get(self, query_args):
        logger.info('GET /product_scraps called')
        logger.debug(f"Query Arguments={query_args}")

        query = ProductScrap.query
        # for filtering
        if 'product_part_no' in query_args:
            query = query.filter(ProductScrap.product_part_no.like(f"%{query_args['product_part_no']}%"))
        if 'start_date' in query_args:
            query = query.filter(ProductScrap.date >= query_args['start_date'])
        if 'end_date' in query_args:
            query = query.filter(ProductScrap.date <= query_args['end_date'])
        if 'min_quantity' in query_args:
            query = query.filter(ProductScrap.quantity >= query_args['min_quantity'])
        if 'max_quantity' in query_args:
            query = query.filter(ProductScrap.quantity <= query_args['max_quantity'])
        if 'scrap_type' in query_args:
            query = query.filter(ProductScrap.scrap_type.like(f"%{query_args['scrap_type']}%"))
        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                ProductScrap.product_part_no.like(search),
                ProductScrap.scrap_type.like(search)
            ))
        # for sorting
        product_scraps, records_count = apply_sorting(query, query_args)
        logger.info(f"Found {records_count} product scraps")
        logger.debug(f"Returned product scraps: {product_scraps}")

        meta = generate_meta(records_count, query_args)
        return product_scraps, {'meta': meta}

    @product_scrap_bp.response(201, ProductScrapSchema)
    @product_scrap_bp.arguments(ProductScrapSchema)
    def post(self, new_product_scrap_data):
        logger.debug(f"Creating new product scrap with args: {new_product_scrap_data}")

        try:
            new_product_scrap = ProductScrap(new_product_scrap_data)
            db.session.add(new_product_scrap)
            db.session.commit()
            logger.info(f"New product scrap created with product_part_no {new_product_scrap.product_part_no} and date "
                        f"{new_product_scrap.date}")
            return new_product_scrap, 201
        except Exception as e:
            logger.error(f"Error creating product scrap: {e}")
            abort(500, message="An error occurred while creating the product scrap")


@product_scrap_bp.route('/product_scrap/<int:product_part_no>/<date:date>')
class ProductScrapResource(MethodView):
    @product_scrap_bp.response(200, ProductScrapSchema)
    def get(self, product_part_no, date):
        logger.info(f"GET /product_scraps/{product_part_no}/{date} called")
        product_scrap = ProductScrap.query.filter_by(product_part_no=product_part_no, date=date).first_or_404(
            description="Product scrap not found")
        logger.info(f"Found product scrap with product_part_no {product_part_no} and date {date}")
        return product_scrap

    @product_scrap_bp.response(200, ProductScrapSchema)
    @product_scrap_bp.arguments(ProductScrapUpdateSchema)
    def put(self, update_product_scrap_data, product_part_no, date):
        logger.info(f"PUT /product_scraps/{product_part_no}/{date} called")
        logger.debug(f"Updating product scrap {product_part_no}/{date} with args: {update_product_scrap_data}")

        product_scrap = ProductScrap.query.filter_by(product_part_no=product_part_no, date=date).first_or_404(
            description="Product scrap not found")
        for key, value in update_product_scrap_data.items():
            setattr(product_scrap, key, value)

        try:
            db.session.commit()
            logger.info(f"Product scrap {product_part_no}/{date} updated")
            return product_scrap
        except Exception as e:
            logger.error(f"Error updating product scrap {product_part_no}/{date}: {e}")
            abort(500, message="An error occurred while updating the product scrap")

    @product_scrap_bp.response(204)
    def delete(self, product_part_no, date):
        logger.info(f"DELETE /product_scraps/{product_part_no}/{date} called")
        product_scrap = ProductScrap.query.filter_by(product_part_no=product_part_no, date=date).first_or_404(
            description="Product scrap not found")
        try:
            db.session.delete(product_scrap)
            db.session.commit()
            logger.info(f"Product scrap {product_part_no}/{date} deleted")
            return {'message': 'Product scrap deleted'}
        except Exception as e:
            logger.error(f"Error deleting product scrap {product_part_no}/{date}: {e}")
            abort(500, message="An error occurred while deleting the product scrap")
