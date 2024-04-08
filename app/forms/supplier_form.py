from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class SupplierForm(FlaskForm):
    name = StringField('Supplier Name', validators=[DataRequired(), Length(max=50)])
    GST_No = StringField('GST No.', validators=[DataRequired(), Length(min=15, max=15)])
    state_code = IntegerField('State Code', validators=[DataRequired(), NumberRange(min=1, max=35)])
    state_name = StringField('State Name', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Add')

    def populate_obj(self, obj):
        obj.name = self.name.data
        obj.GST_No = self.GST_No.data
        obj.state_code = self.state_code.data
        obj.state_name = self.state_name.data
