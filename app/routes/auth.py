from flask import Blueprint, redirect, url_for, request, render_template, flash, jsonify
from flask_security import ForgotPasswordForm, current_user, LoginForm, login_user

from app.errors.not_found_error import NotFoundError
from app.forms.password_form import VerifySecurityForm, ResetPasswordFormModify
from app.logger import logger
from app.services.user_service import UserService

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
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        user = None
        # Try to fetch user by username or email
        user = UserService.get_user_by_username(login) or UserService.get_user_by_email(login)
        if not user:
            flash('User does not exist', 'warning')
            return redirect(url_for('auth.login'))
        try:
            tokens = UserService.authenticate_user(user, password)
            login_user(user)
            UserService.update_user_tracking(user)
            return jsonify(tokens), 200
        except ValueError as ve:
            flash(str(ve), 'warning')
            return redirect(url_for('auth.login'))


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
