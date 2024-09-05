from typing import Optional

from sqlalchemy.orm import joinedload

from app.utils import apply_person_filters, apply_person_sorting
from app.errors.not_found_error import NotFoundError
from app.models import Supplier
from app.extensions import db


class SupplierRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = Supplier.query.options(joinedload(Supplier.state))

        # Apply filters
        query = apply_person_filters(query, Supplier, filters)
        query = apply_person_sorting(query, Supplier, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(supplier_id: int) -> Optional[Supplier]:
        return Supplier.query.get(supplier_id)

    @staticmethod
    def add(supplier: Supplier) -> Supplier:
        db.session.add(supplier)
        db.session.commit()
        return supplier

    @staticmethod
    def update(supplier: Supplier) -> Supplier:
        db.session.commit()
        return supplier

    @staticmethod
    def delete(supplier_id: int) -> None:
        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            raise NotFoundError(f"Bill with id {supplier_id} not found")

        db.session.delete(supplier)
        db.session.commit()
