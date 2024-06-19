from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.extensions import db
from app.logger import logger
from app.models import ProductMaterial
from app.schemas.product_material_schema import ProductMaterialSchema, ProductMaterialUpdateSchema

product_material_bp = Blueprint('product_material_bp', __name__)


@product_material_bp.route('/product_material')
class ProductMaterialListResource(MethodView):

    @product_material_bp.response(201, ProductMaterialSchema)
    @product_material_bp.arguments(ProductMaterialSchema)
    def post(self, new_product_material_data):
        logger.info('POST /product_materials called')
        logger.debug(f"Creating new product material with args: {new_product_material_data}")

        try:
            new_product_material = ProductMaterial(**new_product_material_data)
            db.session.add(new_product_material)
            db.session.commit()
            logger.info(
                f"New product material created with product_part_no {new_product_material.product_part_no} and "
                f"material_part_no {new_product_material.material_part_no}")
            return new_product_material
        except Exception as e:
            logger.error(f"Error creating product material: {e}")
            abort(500, message="An error occurred while creating the product material")


@product_material_bp.route('/product_material/<int:product_part_no>/<int:material_part_no>')
class ProductMaterialResource(MethodView):
    @product_material_bp.response(200, ProductMaterialSchema)
    def get(self, product_part_no, material_part_no):
        logger.info(f"GET /product_materials/{product_part_no}/{material_part_no} called")
        product_material = ProductMaterial.query.filter_by(product_part_no=product_part_no,
                                                           material_part_no=material_part_no).first_or_404(
            description="Product material not found")
        logger.info(
            f"Found product material with product_part_no {product_part_no} and material_part_no {material_part_no}")
        return product_material

    @product_material_bp.response(200, ProductMaterialSchema)
    @product_material_bp.arguments(ProductMaterialUpdateSchema)
    def put(self, update_product_material_data, product_part_no, material_part_no):
        logger.info(f"PUT /product_materials/{product_part_no}/{material_part_no} called")
        logger.debug(
            f"Updating product material {product_part_no}/{material_part_no} with args: {update_product_material_data}")

        product_material = ProductMaterial.query.filter_by(product_part_no=product_part_no,
                                                           material_part_no=material_part_no).first_or_404(
            description="Product material not found")

        for key, value in update_product_material_data.items():
            setattr(product_material, key, value)

        try:
            db.session.commit()
            logger.info(f"Product material {product_part_no}/{material_part_no} updated")
            return product_material
        except Exception as e:
            logger.error(f"Error updating product material {product_part_no}/{material_part_no}: {e}")
            abort(500, message="An error occurred while updating the product material")

    @product_material_bp.response(204)
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
