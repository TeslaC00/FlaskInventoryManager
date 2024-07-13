from typing import Optional

from sqlalchemy import or_

from app.utils import apply_generic_sorting
from app.errors.not_found_error import NotFoundError
from app.extensions import db
from app.models import ChallanItem


class ChallanItemRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = ChallanItem.query
        # for filtering
        if 'challan_id' in filters:
            query = query.filter(ChallanItem.challan_id.like(f"%{filters['challan_id']}%"))
        if 'material_part_no' in filters:
            query = query.filter(ChallanItem.material_part_no.like(f"%{filters['material_part_no']}%"))
        # for searching
        if 'search' in filters:
            search = f"%{filters['search']}%"
            query = query.filter(or_(
                ChallanItem.price.like(search),
                ChallanItem.quantity.like(search),
                ChallanItem.challan_id.like(search),
                ChallanItem.material_part_no.like(search)
            ))
        query = apply_generic_sorting(query, ChallanItem, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(challan_item_id: int) -> Optional[ChallanItem]:
        return ChallanItem.query.get(challan_item_id)

    @staticmethod
    def add(challan_item: ChallanItem) -> ChallanItem:
        db.session.add(challan_item)
        db.session.commit()
        return challan_item

    @staticmethod
    def update(challan_item: ChallanItem) -> ChallanItem:
        db.session.commit()
        return challan_item

    @staticmethod
    def delete(challan_item_id: int) -> None:
        challan_item = ChallanItem.query.get(challan_item_id)
        if not challan_item:
            raise NotFoundError(f"ChallanItem with id {challan_item_id} not found")

        db.session.delete(challan_item)
        db.session.commit()
