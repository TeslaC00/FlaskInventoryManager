from typing import Optional

from sqlalchemy import or_

from app.utils import apply_generic_sorting
from app.models import MaterialScrap
from app.extensions import db
from app.errors.not_found_error import NotFoundError


class MaterialScrapRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = MaterialScrap.query
        # Apply filtering
        if 'material_scrap_part_no' in filters:
            query = query.filter(MaterialScrap.material_scrap_part_no.like(f"%{filters['material_scrap_part_no']}%"))
        if 'start_date' in filters:
            query = query.filter(MaterialScrap.date >= filters['start_date'])
        if 'end_date' in filters:
            query = query.filter(MaterialScrap.date <= filters['end_date'])
        if 'min_quantity' in filters:
            query = query.filter(MaterialScrap.quantity >= filters['min_quantity'])
        if 'max_quantity' in filters:
            query = query.filter(MaterialScrap.quantity <= filters['max_quantity'])
        if 'scrap_type' in filters:
            query = query.filter(MaterialScrap.scrap_type.like(f"%{filters['scrap_type']}%"))
        # Apply searching
        if 'search' in filters:
            search = f"%{filters['search']}%"
            query = query.filter(or_(
                MaterialScrap.material_scrap_part_no.like(search),
                MaterialScrap.scrap_type.like(search)
            ))
        query = apply_generic_sorting(query, MaterialScrap, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(material_part_no: int, date: str) -> Optional[MaterialScrap]:
        return MaterialScrap.query.filter_by(material_part_no=material_part_no, date=date).first()

    @staticmethod
    def add(material_scrap: MaterialScrap) -> MaterialScrap:
        db.session.add(material_scrap)
        db.session.commit()
        return material_scrap

    @staticmethod
    def update(material_scrap: MaterialScrap) -> MaterialScrap:
        db.session.commit()
        return material_scrap

    @staticmethod
    def delete(material_part_no: int, date: str) -> None:
        material_scrap = MaterialScrap.query.filter_by(material_part_no=material_part_no, date=date).first()
        if not material_scrap:
            raise NotFoundError(f"MaterialScrap with id {material_part_no, date} not found")

        db.session.delete(material_scrap)
        db.session.commit()
