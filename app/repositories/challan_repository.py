from typing import Optional

from sqlalchemy import or_

from app.api.utils import apply_generic_sorting
from app.extensions import db
from app.models import Challan


class ChallanRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = Challan.query
        # for filtering
        if 'supplier_id' in filters:
            query = query.filter(Challan.supplier_id.like(f"%{filters['supplier_id']}%"))
        if 'challan_no' in filters:
            query = query.filter(Challan.challan_no.like(f"%{filters['challan_no']}%"))
        if 'start_date' in filters:
            query = query.filter(Challan.date >= filters['start_date'])
        if 'end_date' in filters:
            query = query.filter(Challan.date <= filters['end_date'])
        if 'min_total_price' in filters:
            query = query.filter(Challan.total_price >= filters['min_total_price'])
        if 'max_total_price' in filters:
            query = query.filter(Challan.total_price <= filters['max_total_price'])
        # for searching
        if 'search' in filters:
            search = f"%{filters['search']}%"
            query = query.filter(or_(
                Challan.challan_no.like(search),
                Challan.supplier_id.like(search),
                Challan.total_price.like(search),
                Challan.remarks.like(search)
            ))
        query = apply_generic_sorting(query, Challan, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(challan_id: int) -> Optional[Challan]:
        return Challan.query.get(challan_id)

    @staticmethod
    def add(challan: Challan) -> Challan:
        db.session.add(challan)
        db.session.commit()
        return challan

    @staticmethod
    def update(challan: Challan) -> Challan:
        db.session.commit()
        return challan

    @staticmethod
    def delete(challan_id: int) -> None:
        challan = Challan.query.get(challan_id)
        if not challan:
            raise ValueError(f'Challan with id {challan} not found')

        db.session.delete(challan)
        db.session.commit()
