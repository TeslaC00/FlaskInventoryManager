from flask import Flask, request, render_template, Blueprint, redirect, url_for
from app.logger import logger as log
from app.forms.bill_wtform import SalesForm

bill = Blueprint('bill', __name__)


@bill.route('/api/sales', methods=['GET', 'POST'])
def sales():
    form = SalesForm()

    if form.validate_on_submit():
        # Static fields can be accessed directly
        gst_no = form.gst_no.data

        # For dynamic fields, you might access them like this:
        items = []
        for key in request.form:
            if key.startswith('item'):
                item_id = key[4:]  # Extract the numeric part of the item ID
                rate = request.form.get(f'rate{item_id}', 0)
                quantity = request.form.get(f'quantity{item_id}', 0)
                items.append({'item_id': item_id, 'rate': rate, 'quantity': quantity})
        log.info(items)
        # Process your form data here
        # ...

        return redirect(url_for('success'))  # Assuming you have a success endpoint

    return render_template('orders.html', form=form)
