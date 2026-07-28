from flask_security import ResetPasswordForm
from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired


class VerifySecurityForm(FlaskForm):
    question_id = IntegerField('Question ID', validators=[DataRequired()])
    security_answer = StringField('Security Answer', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Verify Security QA')


class ResetPasswordFormModify(ResetPasswordForm):
    email = StringField('Email', validators=[DataRequired()])
