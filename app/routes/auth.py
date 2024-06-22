from flask import Blueprint, redirect, url_for
from flask_security import current_user

from app.logger import logger

# path for authentication related pages
auth_bp = Blueprint('auth', __name__)


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
