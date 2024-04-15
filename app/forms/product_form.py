from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from app.models import Product


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=50)])
    part_no = IntegerField('Part Number', validators=[DataRequired()])
    unit_type = StringField('Unit Type', validators=[DataRequired(), Length(max=10)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add')

    def populate_obj(self, obj):
        obj.name = self.name
        obj.part_no = self.part_no
        obj.unit_type = self.unit_type
        obj.quantity = self.quantity

    def validate_name(self, field):
        if Product.query.filter_by(name=field.data).first():
            raise ValidationError(f'Product name "{field.data}" already exists')
