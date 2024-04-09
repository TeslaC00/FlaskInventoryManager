from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, FieldList, FormField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Optional


class ItemForm(FlaskForm):
    # Assuming items have a name, rate, and quantity
    name = StringField('Item Name', validators=[DataRequired()])
    rate = DecimalField('Rate', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])


class SalesForm(FlaskForm):
    gst_no = StringField('GST No', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    bill_no = IntegerField('Bill No', validators=[DataRequired()])
    # Dynamic items handled in HTML/JS, processed in Flask route
    items = FieldList(FormField(ItemForm), min_entries=1)  # Example with a single entry; adjust as needed
    sgst = DecimalField('SGST (%)', validators=[DataRequired(), NumberRange(min=0)])
    cgst = DecimalField('CGST (%)', validators=[DataRequired(), NumberRange(min=0)])
    igst = DecimalField('IGST (%)', validators=[Optional(), NumberRange(min=-1)])  # Making the field optional when its value is 0
    submit = SubmitField('Submit')

# Note: You might need to adapt the HTML generation to integrate with Flask-WTForms properly,
# especially for dynamically added fields.
