from datetime import timedelta

from flask import Blueprint, redirect, url_for, request, render_template, flash, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt, \
    decode_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, verify_jwt_in_request
from flask_security import ForgotPasswordForm, LoginForm

from app.errors.not_found_error import NotFoundError
from app.extensions import jwt
from app.forms.password_form import VerifySecurityForm, ResetPasswordFormModify
from app.services.security_question_service import SecurityQuestionService
from app.services.user_service import UserService

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

# path for authentication related pages
auth_bp = Blueprint('auth', __name__)

# In-memory blacklist
# change to redis or database
blacklist = set()


def add_token_to_blacklist(token):
    blacklist.add(token)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
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
    response = make_response(jsonify(refresh=True))
    set_access_cookies(response=response, encoded_access_token=new_access_token)
    return jsonify({'message': 'Token refreshed'})


@auth_bp.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            response = make_response(jsonify(login=True))
            return response, 200

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = UserService.get_user_by_username(username) if username else UserService.get_user_by_email(email)

        if not user:
            flash('User does not exists', 'warning')
            return jsonify({'message': 'User does not exist'}), 400
        try:
            if UserService.authenticate_user(user, password):
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id),
                                                     expires_delta=timedelta(days=30) if remember else timedelta(
                                                         days=1))
                # remove, it uses session we are using JWT(sessionless)
                # login_user(user)
                UserService.update_user_tracking(user)
                response = make_response(jsonify(login=True))
                set_access_cookies(response=response, encoded_access_token=access_token, max_age=MINUTE)
                set_refresh_cookies(response=response, encoded_refresh_token=refresh_token, max_age=DAY)

                return response, 200
            else:
                flash('Invalid password', 'warning')
                return jsonify(login=False), 401
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
                questions = user.questions
                question_form = VerifySecurityForm()
                return render_template('security_question.html', question=questions, email=email,
                                       question_form=question_form)
            else:
                flash('User with given Email Address does not exists', 'warning')
    return render_template('forgot_password.html', form=form)


@auth_bp.route('/verify_security', methods=['POST'])
def verify_security():
    if request.method == 'POST':
        question_form = VerifySecurityForm(request.form)
        if question_form.validate_on_submit():
            question_id = question_form.question_id
            email = question_form.email.data
            user = UserService.get_user_by_email(email)
            if not user:
                flash('User with given Email Address does not exists', 'warning')
            if SecurityQuestionService.verify_answer(user.id, question_id, question_form.security_answer):
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

    response = jsonify({"msg": "logout successful"})

    unset_jwt_cookies(response=response)

    user_id = get_jwt_identity()
    user = UserService.get_user_by_id(user_id)
    UserService.update_user_tracking(user)

    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))
