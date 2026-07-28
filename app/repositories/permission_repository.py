from typing import Optional

from app.errors.not_found_error import NotFoundError
from app.extensions import db
from app.models import Permission


class PermissionRepository:
    @staticmethod
    def get_all():
        return Permission.query.all()

    @staticmethod
    def get_by_id(permission_id: int) -> Optional[Permission]:
        return Permission.query.get(permission_id)

    @staticmethod
    def add(permission: Permission) -> Permission:
        db.session.add(permission)
        db.session.commit()
        return permission

    @staticmethod
    def update(permission: Permission) -> Permission:
        db.session.commit()
        return permission

    @staticmethod
    def delete(permission_id: int) -> None:
        permission = Permission.query.get(permission_id)
        if not permission:
            raise NotFoundError(f"Permission with id {permission_id} not found")

        db.session.delete(permission)
        db.session.commit()
