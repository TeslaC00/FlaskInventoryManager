from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, current_user

import app
from app.forms.login_form import LoginForm
from app.models import User

# path for authentication related pages
auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()

# To display warning if user is not logged in and try to access other pages
login_manager.login_view = 'auth.login_page'


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


@auth_bp.route('/')
def login_page():
    """
    Renders the base page when user is authenticated, otherwise redirects to the login page
    :return: Response: rendered login.html
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.root'))
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth_bp.route('/login/', methods=['POST', 'GET'])
def login():
    """
    Authenticates user based on the username and password provided in the form

    If provided credentials are valid, login the user and redirects to the base page.
    If user is invalid then flashes invalid user message then redirects to login page.
    :return: Response: Redirect to base page if authentication succeeds, otherwise redirects to login page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        app.app.logger.debug(user)
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.root'))
        else:
            flash('Invalid username or password')
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/logout')
def logout():
    """
    Logs out the current user, clears the session and redirects to the login page
    :return: Response: Redirect to login page
    """
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))
