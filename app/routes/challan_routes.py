from flask import Blueprint, request, render_template

from app.forms.challan_form import PurchaseForm
from app.logger import logger as log
from app.models.challan import Challan

challan = Blueprint('challan', __name__)


@challan.route('/api/add_challan', methods=['GET', 'POST'])
def add_challan():
    purchase_form = PurchaseForm()
    log.info('called Add challan')

    log.info(f'purchase_form submit: {purchase_form.submit}')
    log.info(f'purchase_form validation: {purchase_form.validate()}')
    log.info(f'purchase_form validation: {purchase_form.errors}')

    if request.method == 'POST' and purchase_form.validate_on_submit():
        # Process validated purchase_form data
        log.info('validated purchase_form')
        challan = Challan(
            challan_no=purchase_form.challan_no.data,
            supplier_id=purchase_form.supplier_id.data,
            material_name=purchase_form.supplier_name.data,
            price=1,
            quantity=1,
            date=purchase_form.date.data,
        )
        log.info(challan.to_dict())
        form_date = request.form.to_dict(flat=False)
        log.info(form_date)

        # Redirect or inform of successful submission, etc.
        return 'Form Submitted'

    return render_template('addentry.html', form=purchase_form)

@challan.route('/api/challan_get', methods=['GET', 'POST'])
def get_challan():
    return render_template('show_challans.html')





