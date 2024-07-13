from typing import Optional

from sqlalchemy import or_

from app.utils import apply_generic_sorting
from app.models import ProductScrap
from app.extensions import db
from app.errors.not_found_error import NotFoundError


class ProductScrapRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = ProductScrap.query
        # Apply filters
        if 'product_part_no' in filters:
            query = query.filter(ProductScrap.product_part_no.like(f"%{filters['product_part_no']}%"))
        if 'start_date' in filters:
            query = query.filter(ProductScrap.date >= filters['start_date'])
        if 'end_date' in filters:
            query = query.filter(ProductScrap.date <= filters['end_date'])
        if 'min_quantity' in filters:
            query = query.filter(ProductScrap.quantity >= filters['min_quantity'])
        if 'max_quantity' in filters:
            query = query.filter(ProductScrap.quantity <= filters['max_quantity'])
        if 'scrap_type' in filters:
            query = query.filter(ProductScrap.scrap_type.like(f"%{filters['scrap_type']}%"))
        # Apply search
        if 'search' in filters:
            search = f"%{filters['search']}%"
            query = query.filter(or_(
                ProductScrap.product_part_no.like(search),
                ProductScrap.scrap_type.like(search)
            ))
        query = apply_generic_sorting(query, ProductScrap, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(product_scrap_id: int) -> Optional[ProductScrap]:
        return ProductScrap.query.get(product_scrap_id)

    @staticmethod
    def add(product_scrap: ProductScrap) -> ProductScrap:
        db.session.add(product_scrap)
        db.session.commit()
        return product_scrap

    @staticmethod
    def update(product_scrap: ProductScrap) -> ProductScrap:
        db.session.commit()
        return product_scrap

    @staticmethod
    def delete(product_scrap_id: int) -> None:
        product_scrap = ProductScrap.query.get(product_scrap_id)
        if not product_scrap:
            raise NotFoundError(f"ProductScrap with id {product_scrap_id} not found")

        db.session.delete(product_scrap)
        db.session.commit()
