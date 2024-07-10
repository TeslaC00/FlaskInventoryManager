from flask import Blueprint, redirect, url_for, request, render_template, flash
from flask_security import ForgotPasswordForm, current_user, hash_password
from flask import current_app

from app.forms.password_form import VerifySecurityForm, ResetPasswordFormModify
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


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            user = current_app.security.datastore.db.User.query.filter_by(email=email).first()
            if user:
                question = user.security_question
                question_form = VerifySecurityForm()
                return render_template('security_question.html', question=question, email=email,
                                       question_form=question_form)
            else:
                flash('Email Address not found', 'warning')
    return render_template('forgot_password.html', form=form)


@auth_bp.route('/verify_security', methods=['POST'])
def verify_security():
    if request.method == 'POST':
        question_form = VerifySecurityForm(request.form)
        if question_form.validate_on_submit():
            email = question_form.email.data
            user = current_app.security.datastore.db.User.query.filter_by(email=email).first()
            if user and question_form.security_answer == user.security_answer:
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
            user = current_app.security.datastore.db.User.query.filter_by(email=email).first()
            hashed_password = hash_password(password)
            user.password = hashed_password
            flash('Your password has been updated!', 'success')
            return redirect(url_for('security.login'))
    redirect(url_for('forgot_password'))
