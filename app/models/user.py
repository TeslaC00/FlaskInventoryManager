# user.py
from flask_security import UserMixin, RoleMixin, AsaList
from app.extensions import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship, backref
from app.extensions import bcrypt


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id'))
    role_id = Column(Integer(), ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """
        Creates a dictionary representation of the User instance, including the username, password, and user type.

        Returns:
            dict: A dictionary containing the user's 'username', 'password', and 'user_type'.
        """
        return {

        }

    # def get_id(self):
    #     """
    #     Overrides the `get_id` method from UserMixin, utilizing the username as the unique identifier
    #     for the user session.
    #
    #     Returns:
    #         str: The username of the user, serving as the unique identifier.
    #     """
    #     return self.username
