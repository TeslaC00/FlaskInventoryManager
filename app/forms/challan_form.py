from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    name = StringField('Raw Material', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])


class PurchaseForm(FlaskForm):
    supplier_id = StringField('Supplier ID', validators=[DataRequired()])
    supplier_name = StringField('Supplier Name', validators=[DataRequired()])   # TODO: it's not in model why here?
    challan_no = StringField('Challan No.', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])  # Consider using DateField
    items = FieldList(FormField(ItemForm), min_entries=0)
    submit = SubmitField('Submit')
