from flask import render_template, redirect, Blueprint

from app.database import db
from app.models import User

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/')
def show_users():
    """
    Route to display a list of all users.

    Fetches all user records from the database and renders them on the 'user.html' template.

    Returns:
        Rendered template ('user.html') with all users passed as context.
    """
    users = User.query.all()
    return render_template('user.html', users=users)


@user_bp.route('/<user_type>/')
def show_users_by_type(user_type):
    """
    Route to display users filtered by their type.

    Parameters:
        user_type (str): The type of users to filter by.

    Fetches user records from the database that match the specified type and renders them on the 'user.html' template.

    Returns:
        Rendered template ('user.html') with filtered users passed as context.
    """
    users = User.query.filter(User.user_type == user_type).all()
    return render_template('user.html', users=users)


@user_bp.route('/find/<username>')
def show_users_by_username(username):
    """
    Route to display users filtered by username.

    Parameters:
        username (str): The username to filter users by.

    Fetches user records from the database that match the specified username and renders them on the 'user.html' template.

    Returns:
        Rendered template ('user.html') with filtered users passed as context.
    """
    users = User.query.filter(User.username == username).all()
    return render_template('user.html', users=users)


@user_bp.route('/<user_name>/<password>/<user_type>/')
def add_user(user_name, password, user_type):
    """
    Route to add a new user to the database.

    Parameters:
        user_name (str): The username of the new user.
        password (str): The password for the new user.
        user_type (str): The type of the new user.

    Creates a new User instance with the provided username, password, and user type, adds it to the database,
    commits the session, and then redirects to the users listing page.

    Returns:
        A redirection to the users listing page ('/users/').
    """
    user = User(username=user_name, password=password, user_type=user_type)
    db.session.add(user)
    db.session.commit()
    return redirect('/users/')
