from datetime import timedelta

from flask import Blueprint, redirect, url_for, request, render_template, flash, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt, \
    decode_token
from flask_security import ForgotPasswordForm, LoginForm, login_user, url_for_security

from app.errors.not_found_error import NotFoundError
from app.extensions import jwt
from app.forms.password_form import VerifySecurityForm, ResetPasswordFormModify
from app.logger import logger
from app.services.user_service import UserService

# path for authentication related pages
auth_bp = Blueprint('auth', __name__)

# In-memory blacklist
# change to redis or database
blacklist = set()


def add_token_to_blacklist(token):
    blacklist.add(token)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@auth_bp.route('/verify_token', methods=['GET'])
@jwt_required()
def verify_token():
    user_identity = get_jwt_identity()  # Get the user identity from the token
    return jsonify(user_id=user_identity), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    jti = get_jwt()['jti']  # Get the ID of the current refresh token
    add_token_to_blacklist(jti)  # Blacklist the old refresh token

    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify(access_token=new_access_token)


# @auth_bp.route('/')
# def index():
#     """
#     Renders the base page when user is authenticated, otherwise redirects to the login page
#     :return: Response: rendered login.html
#     """
#     # may need to create own login form to keep it sessionless
#     return redirect(url_for('auth.login'))


@auth_bp.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = None
        if username:
            user = UserService.get_user_by_username(username)
        if email:
            user = UserService.get_user_by_email(email)
        if not user:
            flash('User does not exists', 'warning')
            return jsonify({'message': 'User does not exist'}), 400
        try:
            if UserService.authenticate_user(user, password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id,
                                                     expires_delta=timedelta(days=30) if remember else timedelta(
                                                         days=1))
                # remove, it uses session we are using JWT(sessionless)
                # login_user(user)
                UserService.update_user_tracking(user)
                return jsonify(access_token=access_token, refresh_token=refresh_token), 200
            else:
                flash('Invalid password', 'warning')
                return jsonify({'message': 'Invalid password'}), 401
        except ValueError as ve:
            flash(str(ve), 'warning')
            return jsonify({'message': 'Form validation failed'}), 400
    return render_template('security/login_user.html', login_user_form=form, identity_attributes=['email', 'username'])


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            user = UserService.get_user_by_email(email)
            if user:
                question = user.question
                question_form = VerifySecurityForm()
                return render_template('security_question.html', question=question, email=email,
                                       question_form=question_form)
            else:
                flash('User with given Email Address does not exists', 'warning')
    return render_template('forgot_password.html', form=form)


@auth_bp.route('/verify_security', methods=['POST'])
def verify_security():
    if request.method == 'POST':
        question_form = VerifySecurityForm(request.form)
        if question_form.validate_on_submit():
            email = question_form.email.data
            user = UserService.get_user_by_email(email)
            if not user:
                flash('User with given Email Address does not exists', 'warning')
            if UserService.authenticate_user_answer(user, question_form.security_answer):
                return render_template('reset_password.html', form=ResetPasswordFormModify(), email=email)
            else:
                flash('Security Answer not match', 'warning')
                return redirect(url_for('security.login'))
    return redirect(url_for('verify_security'))


@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    if request.method == 'POST':
        form = ResetPasswordFormModify(request.form)
        if form.validate_on_submit():
            password = form.password.data
            email = form.email.data
            user = UserService.get_user_by_email(email)
            try:
                UserService.reset_password(user, password)
                flash('Your password has been updated!', 'success')
                return redirect(url_for('security.login'))
            except NotFoundError as nfe:
                flash(str(nfe), 'warning')
    redirect(url_for('forgot_password'))


@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)

    # Handle refresh token blacklisting
    refresh_token = request.cookies.get('refresh_token')
    jti_refresh = decode_token(refresh_token)['jti']  # Extract jti from refresh token
    add_token_to_blacklist(jti_refresh)  # Blacklist the refresh token

    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)
    UserService.update_user_tracking(user)

    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))
