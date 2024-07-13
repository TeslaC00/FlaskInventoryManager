from typing import Optional

from app.api.utils import apply_generic_sorting
from app.errors.not_found_error import NotFoundError
from app.models import ProductionLog
from app.extensions import db


class ProductionLogRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = ProductionLog.query

        # Apply filtering
        if 'product_part_no' in filters:
            query = query.filter(ProductionLog.product_part_no.like(f"%{filters['product_part_no']}%"))
        if 'start_date' in filters:
            query = query.filter(ProductionLog.production_date >= filters['start_date'])
        if 'end_date' in filters:
            query = query.filter(ProductionLog.production_date <= filters['end_date'])
        if 'min_quantity' in filters:
            query = query.filter(ProductionLog.quantity_produced >= filters['min_quantity'])
        if 'max_quantity' in filters:
            query = query.filter(ProductionLog.quantity_produced <= filters['max_quantity'])
        # Apply sorting
        query = apply_generic_sorting(query, ProductionLog, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(production_log_id: int) -> Optional[ProductionLog]:
        return ProductionLog.query.get(production_log_id)

    @staticmethod
    def add(production_log: ProductionLog) -> ProductionLog:
        db.session.add(production_log)
        db.session.commit()
        return production_log

    @staticmethod
    def update(production_log: ProductionLog) -> ProductionLog:
        db.session.commit()
        return production_log

    @staticmethod
    def delete(production_log_id: int) -> None:
        production_log = ProductionLog.query.get(production_log_id)
        if not production_log:
            raise NotFoundError(f"ProductionLog with id {production_log_id} not found")

        db.session.delete(production_log)
        db.session.commit()
