from typing import Optional

from app.api.utils import apply_generic_sorting
from app.errors.not_found_error import NotFoundError
from app.extensions import db
from app.models import Material


class MaterialRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = Material.query
        # Apply filters
        if 'name' in filters:
            query = query.filter(Material.name.like(f"%{filters['name']}%"))
        if 'unit_id' in filters:
            query = query.filter(Material.unit_id == filters['unit_id'])
        if 'min_quantity' in filters:
            query = query.filter(Material.quantity >= filters['min_quantity'])
        if 'max_quantity' in filters:
            query = query.filter(Material.quantity <= filters['max_quantity'])
        # for searching
        if 'search' in filters:
            query = query.filter(Material.name.like(f"%{filters['search']}%"))
        query = apply_generic_sorting(query, Material, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(material_id: int) -> Optional[Material]:
        return Material.query.get(material_id)

    @staticmethod
    def add(material: Material) -> Material:
        db.session.add(material)
        db.session.commit()
        return material

    @staticmethod
    def update(material: Material) -> Material:
        db.session.commit()
        return material

    @staticmethod
    def delete(material_id: int) -> None:
        material = Material.query.get(material_id)
        if not material:
            raise NotFoundError(f"Material with id {material_id} not found")

        db.session.delete(material)
        db.session.commit()
