from typing import Optional

from app.extensions import db
from app.models import Bill


class BillRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        raise NotImplementedError

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
