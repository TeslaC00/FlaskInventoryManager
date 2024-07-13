from typing import Optional

from flask_security import hash_password, verify_password
from sqlalchemy import or_

from app.utils import apply_generic_sorting
from app.models import User, Role
from app.extensions import db
from app.errors.not_found_error import NotFoundError
from app.datastore import user_datastore


class UserRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = User.query
        # Apply filters
        if 'email' in filters:
            query = query.filter(User.email.like(f"%{filters['email']}%"))
        if 'username' in filters:
            query = query.filter(User.username.like(f"%{filters['username']}%"))
        if 'active' in filters:
            query = query.filter(User.active == filters['active'])

        # for searching
        if 'search' in filters:
            search = f"%{filters['search']}%"
            query = query.filter(or_(
                User.name.like(search),
                User.email.like(search),
            ))
        query = apply_generic_sorting(query, User, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return user_datastore.find_user(id=user_id)

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        return user_datastore.find_user(username=username)

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return user_datastore.find_user(email=email)

    @staticmethod
    def add(**data) -> User:
        user = user_datastore.create_user(data)
        user.password = hash_password(password=user.password)
        db.session.commit()
        return user

    @staticmethod
    def update(user: User) -> User:
        db.session.commit()
        return user

    @staticmethod
    def activate(user: User) -> bool:
        return user_datastore.activate_user(user)

    @staticmethod
    def deactivate(user: User) -> bool:
        return user_datastore.deactivate_user(user)

    @staticmethod
    def add_role(user: User, roles: list[Role]) -> User:
        user.roles = roles
        return user

    @staticmethod
    def delete(user_id: int) -> None:
        user = user_datastore.find_user(id=user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")

        user_datastore.delete_user(user)
        db.session.commit()

    @staticmethod
    def verify_password(user: User, password: str) -> bool:
        return verify_password(password=password, password_hash=user.password)
