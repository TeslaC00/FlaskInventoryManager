from flask import Blueprint, request, render_template

from app.forms.challan_form import PurchaseForm
from app.logger import logger as log
from app.models.challan import Challan

challan = Blueprint('challan', __name__)


@challan.route('/api/add_challan', methods=['GET', 'POST'])
def add_challan():
    form = PurchaseForm()
    log.info('called Add challan')

    if request.method == 'POST' and form.validate_on_submit():
        # Process validated form data
        log.info('validated form')
        challan = Challan(
            challan_no=form.challan_no.data,
            supplier_id=form.supplier_id.data,
            material_name=form.supplier_name.data,
            price=1,
            quantity=1,
            date=form.date.data,
        )
        log.info(challan.to_dict())
        for multipleFields in form.items.entries:
            log.info(multipleFields.data)


        # Redirect or inform of successful submission, etc.
        return 'Form Submitted'

    return render_template('addentry.html', form=form)


