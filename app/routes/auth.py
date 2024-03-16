from flask import Blueprint, render_template, request, redirect, url_for

from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def login_page():
    message = request.args.get('message')
    return render_template('auth/login.html', message=message)


@auth_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        return f'Logged in as {user.username}'
    else:
        return redirect(url_for('auth.login_page', message='Bad Credentials'))
