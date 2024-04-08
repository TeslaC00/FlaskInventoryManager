from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class SupplierForm(FlaskForm):
    name = StringField('Supplier Name', validators=[DataRequired(), Length(max=50)])
    GST_No = StringField('GST No.', validators=[DataRequired(), Length(min=15, max=15)])
    state_code = IntegerField('State Code', validators=[DataRequired(), NumberRange(min=1, max=35)])
    state_name = StringField('State Name', validators=[DataRequired(), Length(max=30)])
