from typing import Optional

from sqlalchemy import or_

from app.api.utils import apply_generic_sorting
from app.errors.not_found_error import NotFoundError
from app.models import BillItem
from app.extensions import db


class BillItemRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = BillItem.query
        # for filtering
        if 'bill_id' in filters:
            query = query.filter(BillItem.bill_id == filters['bill_id'])
        if 'product_part_no' in filters:
            query = query.filter(BillItem.product_part_no == filters['product_part_no'])
        # for searching
        if 'search' in filters:
            search = f"%{filters['search']}%"
            query = query.filter(or_(
                BillItem.quantity.like(search),
                BillItem.price.like(search),
                BillItem.bill_id.like(search),
                BillItem.product_part_no.like(search)
            ))
        query = apply_generic_sorting(query, BillItem, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(bill_item_id: int) -> Optional[BillItem]:
        return BillItem.query.get(bill_item_id)

    @staticmethod
    def add(bill_item: BillItem) -> BillItem:
        db.session.add(bill_item)
        db.session.commit()
        return bill_item

    @staticmethod
    def update(bill_item: BillItem) -> BillItem:
        db.session.commit()
        return bill_item

    @staticmethod
    def delete(bill_item_id: int) -> None:
        bill_item = BillItem.query.get(bill_item_id)
        if not bill_item:
            raise NotFoundError(f"BillItem with id {bill_item_id} not found")

        db.session.delete(bill_item)
        db.session.commit()
