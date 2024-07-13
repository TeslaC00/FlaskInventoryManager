from typing import Optional

from app.errors.not_found_error import NotFoundError
from app.models import ProductMaterial
from app.extensions import db


class ProductMaterialRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10):
        query = ProductMaterial.query
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(product_part_no: int, material_part_no: int) -> Optional[ProductMaterial]:
        return ProductMaterial.query.filter_by(product_part_no=product_part_no,
                                               material_part_no=material_part_no).first()

    @staticmethod
    def add(product_material: ProductMaterial) -> ProductMaterial:
        db.session.add(product_material)
        db.session.commit()
        return product_material

    @staticmethod
    def update(product_material: ProductMaterial) -> ProductMaterial:
        db.session.commit()
        return product_material

    @staticmethod
    def delete(product_part_no: int, material_part_no: int) -> None:
        product_material = ProductMaterial.query.get(product_part_no, material_part_no)
        if not product_material:
            raise NotFoundError(f"ProductMaterial with id {product_part_no, material_part_no} not found")

        db.session.delete(product_material)
        db.session.commit()
