from typing import Optional

from sqlalchemy import or_

from app.errors.not_found_error import NotFoundError
from app.models import Buyer
from app.extensions import db


class BuyerRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = Buyer.query

        # Apply filters
        if 'name' in filters:
            query = query.filter(Buyer.name.like(f"%{filters['name']}%"))
        if 'GST_No' in filters:
            query = query.filter(Buyer.GST_No.like(f"%{filters['GST_No']}%"))
        if 'state_code' in filters:
            query = query.filter(Buyer.state_code.like(f"%{filters['state_code']}%"))
        if 'state_name' in filters:
            query = query.filter(Buyer.state_name.like(f"%{filters['state_name']}%"))
        if 'search' in filters:
            search = f"%{filters['search']}%"
            query = query.filter(or_(
                Buyer.name.like(search),
                Buyer.GST_No.like(search),
                Buyer.state_name.like(search),
                Buyer.address.like(search)
            ))
        # Apply sorting
        if 'sort_by' in filters:
            sort_column = getattr(Buyer, filters['sort_by'], None)
            if sort_column:
                if filters.get('sort_order', 'asc') == 'desc':
                    query = query.order_by(sort_column.desc())
                else:
                    query = query.order_by(sort_column.asc())
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
            raise NotFoundError(f"Bill with id {buyer_id} not found")

        db.session.delete(buyer)
        db.session.commit()
