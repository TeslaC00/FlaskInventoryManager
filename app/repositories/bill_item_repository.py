from typing import Optional

from app.errors.not_found_error import NotFoundError
from app.models import BillItem
from app.extensions import db


class BillItemRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        raise NotImplementedError

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
