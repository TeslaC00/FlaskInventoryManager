from flask import render_template, redirect, Blueprint

from app import db
from app.models import User

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/')
def show_users():
    # Fetch all users from the User table
    users = User.query.all()
    return render_template('user.html', users=users)


@user_bp.route('/<user_type>/')
def show_users_by_type(user_type):
    # Fetch all users from the User table
    users = User.query.filter(User.user_type == user_type).all()
    return render_template('user.html', users=users)


@user_bp.route('/find/<username>')
def show_users_by_username(username):
    users = User.query.filter(User.username == username).all()
    return render_template('user.html', users=users)


@user_bp.route('/<user_name>/<password>/<user_type>/')
def add_user(user_name, password, user_type):
    user = User(username=user_name, password=password, user_type=user_type)
    db.session.add(user)
    db.session.commit()
    return redirect('/users/')
