import random
from datetime import datetime, timedelta

from flask_login import UserMixin

from app.database import db


class User(db.Model, UserMixin):
    """
    Represents a user entity for authentication and authorization within the application, combining
    SQLAlchemy ORM modeling for database interaction and Flask-Login for handling user sessions.
    This model supports user management, including user login processes.

    Attributes:
        __tablename__ (str): Defines the table name in the database for the User model.
        username (db.Column): Stores the username, which serves as a unique identifier for each user.
                              It is a string of maximum length 50 characters and acts as the primary key.
        password (db.Column): Holds the user's password. It is stored as a string of maximum length 50
                              characters and cannot be null, implying that every user must have a password.
        role (db.Column): Defines the type or role of the user within the system (e.g., 'admin', 'editor').
                               It is a string of maximum length 20 characters and cannot be null.

    The model includes a method `to_dict` for converting user entity attributes to a dictionary, suitable
    for JSON serialization or similar use cases. It also overrides the `get_id` method from UserMixin to
    return the username as the unique identifier for Flask-Login.

    Methods:
        to_dict(self): Converts the User instance into a dictionary containing 'username', 'password',
                       and 'user_type' as keys.
        get_id(self): Overrides the UserMixin's `get_id` method to use the username as the unique identifier
                      for Flask-Login's user session management.
    """

    __tablename__ = 'user'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    audit_logs = db.relationship('AuditLog', backref='user')

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        # Generate a random date within the past 30 days for last_login
        # added this for dummy date and time
        self.last_login = datetime.now() - timedelta(days=random.randint(1, 30))

    def to_dict(self):
        """
        Creates a dictionary representation of the User instance, including the username, password, and user type.

        Returns:
            dict: A dictionary containing the user's 'username', 'password', and 'user_type'.
        """
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'last_login': self.last_login,
        }

    def get_id(self):
        """
        Overrides the `get_id` method from UserMixin, utilizing the username as the unique identifier
        for the user session.

        Returns:
            str: The username of the user, serving as the unique identifier.
        """
        return self.username
