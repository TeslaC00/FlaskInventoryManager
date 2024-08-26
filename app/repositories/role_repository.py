from typing import Optional

from app.utils import apply_generic_sorting
from app.models import Role
from app.extensions import db
from app.datastore import user_datastore
from app.errors.not_found_error import NotFoundError


class RoleRepository:
    @staticmethod
    def get_all(**filters: dict):
        query = Role.query

        # Apply filters
        if 'search' in filters:
            query = query.filter(Role.name.like(f"%{filters['search']}%"))
        query = apply_generic_sorting(query, Role, filters)
        return query.all()

    @staticmethod
    def get_by_id(role_id: int) -> Optional[Role]:
        return Role.query.get(role_id)

    @staticmethod
    def add(**data) -> Role:
        return user_datastore.create_role(data)

    @staticmethod
    def update(role: Role) -> Role:
        db.session.commit()
        return role

    @staticmethod
    def delete(role_id: int) -> None:
        role = Role.query.get(role_id)
        if not role:
            raise NotFoundError(f"Bill with id {role_id} not found")
        if role.users:
            raise ValueError(f"Role {role.name} with id {role_id} already in use, cannot be deleted")
        db.session.delete(role)
        db.session.commit()
