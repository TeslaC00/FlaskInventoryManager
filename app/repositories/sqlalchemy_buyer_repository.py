from sqlalchemy import or_, text

from app.models import Buyer
from app.repositories.buyer_repository import BuyerRepository
from app.extensions import db


class SQLAlchemyBuyerRepository(BuyerRepository):
    def get_all(self, filters=None, pagination_parameters=None):
        query = Buyer.query
        if filters:
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
            if 'sort_order' in filters:
                order = 'DESC' if filters['sort_order'] == 'desc' else 'ASC'
                query = query.order_by(text(f"{filters['sort_by']} {order}"))
            pagination_parameters.item_count = query.count()
            page = pagination_parameters.page
            per_page = pagination_parameters.page_size
            query = query.offset((page - 1) * per_page).limit(per_page)
        return query.all()

    def get_by_id(self, buyer_id):
        return Buyer.query.get(buyer_id)

    def add(self, buyer: Buyer):
        db.session.add(buyer)
        db.session.commit()
        return buyer

    def update(self, buyer: Buyer):
        db.session.commit()
        return buyer

    def delete(self, buyer: Buyer):
        db.session.delete(buyer)
        db.session.commit()
