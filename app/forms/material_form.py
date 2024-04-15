from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from app.models import Material


class MaterialForm(FlaskForm):
    name = StringField('Material Name', validators=[DataRequired(), Length(max=50)])
    unit_type = StringField('Unit Type', validators=[DataRequired(), Length(max=10)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add')

    def populate_obj(self, obj):
        obj.name = self.name.data
        obj.unit_type = self.unit_type.data
        obj.quantity = self.quantity.data

    def validate_name(self, name):
        material = Material.query.filter_by(name=name.data).first()
        if material:
            raise ValidationError(f'Material with name "{name.data}" already exists.')
