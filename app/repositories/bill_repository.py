from typing import Optional

from sqlalchemy import or_

from app.utils import apply_generic_sorting
from app.extensions import db
from app.models import Bill


class BillRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = Bill.query
        # for filtering
        if 'buyer_id' in filters:
            query = query.filter(Bill.buyer_id.like(f"%{filters['buyer_id']}%"))
        if 'purchase_order' in filters:
            query = query.filter(Bill.purchase_order.like(f"%{filters['purchase_order']}%"))
        if 'start_date' in filters:
            query = query.filter(Bill.date >= filters['start_date'])
        if 'end_date' in filters:
            query = query.filter(Bill.date <= filters['end_date'])
        if 'min_total_price' in filters:
            query = query.filter(Bill.total_price >= filters['min_total_price'])
        if 'max_total_price' in filters:
            query = query.filter(Bill.total_price <= filters['max_total_price'])
        # for searching
        if 'search' in filters:
            query = query.filter(or_(
                Bill.purchase_order.like(f"%{filters['search']}%"),
                Bill.remarks.like(f"%{filters['search']}%")
            ))
        query = apply_generic_sorting(query, Bill, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(bill_id: int) -> Optional[Bill]:
        return Bill.query.get(bill_id)

    @staticmethod
    def add(bill: Bill) -> Bill:
        db.session.add(bill)
        db.session.commit()
        return bill

    @staticmethod
    def update(bill: Bill) -> Bill:
        db.session.commit()
        return bill

    @staticmethod
    def delete(bill_id: int) -> None:
        bill = Bill.query.get(bill_id)
        if not bill:
            raise ValueError(f'Bill with id {bill} not found')

        db.session.delete(bill)
        db.session.commit()
