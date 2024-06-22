from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_security import login_user, logout_user, current_user

from app.forms.login_form import LoginForm
from app.models import User
from app.logger import logger
# from app.extensions import login_manager

# path for authentication related pages
auth_bp = Blueprint('auth', __name__)

# To display warning if user is not logged in and try to access other pages
# login_manager.login_view = 'auth.login_page'


@auth_bp.route('/')
def login_page():
    """
    Renders the base page when user is authenticated, otherwise redirects to the login page
    :return: Response: rendered login.html
    """
    if current_user.is_authenticated:
        logger.info('User already logged in redirecting to base page')
        return redirect(url_for('main.root'))
    return redirect(url_for('security.login'))
