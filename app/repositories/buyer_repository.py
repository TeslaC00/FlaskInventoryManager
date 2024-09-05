from typing import Optional

from sqlalchemy.orm import joinedload

from app.utils import apply_person_filters, apply_person_sorting
from app.errors.not_found_error import NotFoundError
from app.models import Buyer
from app.extensions import db


class BuyerRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = Buyer.query.options(joinedload(Buyer.state))

        # Apply filters
        query = apply_person_filters(query, Buyer, filters)
        query = apply_person_sorting(query, Buyer, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(buyer_id: int) -> Optional[Buyer]:
        return Buyer.query.get(buyer_id)

    @staticmethod
    def add(buyer: Buyer) -> Buyer:
        db.session.add(buyer)
        db.session.commit()
        return buyer

    @staticmethod
    def update(buyer: Buyer) -> Buyer:
        db.session.commit()
        return buyer

    @staticmethod
    def delete(buyer_id: int) -> None:
        buyer = Buyer.query.get(buyer_id)
        if not buyer:
            raise NotFoundError(f"Buyer with id {buyer_id} not found")

        db.session.delete(buyer)
        db.session.commit()
