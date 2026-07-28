from flask import Blueprint, request, render_template
from app.extensions import db

from app.logger import logger
from app.models.user import User

user = Blueprint('user', __name__)


@user.route('/api/get_users', methods=['GET', 'POST'])
def get_users():
    return render_template('user_table.html')
