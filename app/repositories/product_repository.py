from typing import Optional

from app.api.utils import apply_generic_sorting
from app.errors.not_found_error import NotFoundError
from app.models import Product
from app.extensions import db


class ProductRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = Product.query
        # Apply filters
        if 'name' in filters:
            query = query.filter(Product.name.like(f"%{filters['name']}%"))
        if 'unit_id' in filters:
            query = query.filter(Product.unit_id == filters['unit_id'])
        if 'min_quantity' in filters:
            query = query.filter(Product.quantity >= filters['min_quantity'])
        if 'max_quantity' in filters:
            query = query.filter(Product.quantity <= filters['max_quantity'])
        if 'min_price' in filters:
            query = query.filter(Product.price >= filters['min_price'])
        if 'max_price' in filters:
            query = query.filter(Product.price <= filters['max_price'])
        if 'min_c_gst' in filters:
            query = query.filter(Product.c_gst >= filters['min_c_gst'])
        if 'max_c_gst' in filters:
            query = query.filter(Product.c_gst <= filters['max_c_gst'])
        if 'min_s_gst' in filters:
            query = query.filter(Product.s_gst >= filters['min_s_gst'])
        if 'max_s_gst' in filters:
            query = query.filter(Product.s_gst <= filters['max_s_gst'])
        if 'min_i_gst' in filters:
            query = query.filter(Product.i_gst >= filters['min_i_gst'])
        if 'max_i_gst' in filters:
            query = query.filter(Product.i_gst <= filters['max_i_gst'])
        # for searching
        if 'search' in filters:
            query = query.filter(Product.name.like(f"%{filters['search']}%"))
        query = apply_generic_sorting(query, Product, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(product_id: int) -> Optional[Product]:
        return Product.query.get(product_id)

    @staticmethod
    def add(product: Product) -> Product:
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def update(product: Product) -> Product:
        db.session.commit()
        return product

    @staticmethod
    def delete(product_id: int) -> None:
        product = Product.query.get(product_id)
        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")

        db.session.delete(product)
        db.session.commit()
