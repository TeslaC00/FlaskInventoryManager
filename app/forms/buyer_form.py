from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class BuyerForm(FlaskForm):
    name = StringField('Buyer Name', validators=[DataRequired(), Length(max=50)])
    GST_No = StringField('GST No', validators=[DataRequired(), Length(min=15, max=15)])
    state_code = IntegerField('State Code', validators=[DataRequired(), NumberRange(min=1, max=35)])
    state_name = StringField('State Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add')

    def populate_obj(self, obj):
        obj.name = self.name
        obj.GST_No = self.GST_No
        obj.state_code = self.state_code
        obj.state_name = self.state_name
