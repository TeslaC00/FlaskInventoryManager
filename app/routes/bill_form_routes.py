from flask import Flask, request, render_template, Blueprint, redirect, url_for
from app.logger import logger as log
from app.forms.bill_wtform import SalesForm
from flask_wtf import csrf

bill = Blueprint('bill', __name__)


@bill.route('/api/sales', methods=['GET', 'POST'])
def sales():
    csrf_token = csrf.generate_csrf()
    log.info('Sales route called')
    form = SalesForm()
    log.info('Sales wtform no error')
    if form.validate_on_submit():
        # Static fields can be accessed directly
        log.info('Sales form submitted successfully')
        gst_no = form.gst_no.data
        log.info(f'Sales gst_no: {gst_no}')
        # For dynamic fields, you might access them like this:
        items = []
        for key in request.form:
            if key.startswith('item'):
                item_id = key[4:]  # Extract the numeric part of the item ID
                rate = request.form.get(f'rate{item_id}', 0)
                quantity = request.form.get(f'quantity{item_id}', 0)
                items.append({'item_id': item_id, 'rate': rate, 'quantity': quantity})
        log.info(f'Sales form: {form.data}')
        for i in items:
            log.info(f"{i['item_id']}: {i['rate']} {i['quantity']}")

        return redirect(url_for('bill.sales'))  # Assuming you have a success endpoint
    else:
        log.info(form.errors)
    return render_template('orders.html', form=form,  csrf_token=csrf_token)
