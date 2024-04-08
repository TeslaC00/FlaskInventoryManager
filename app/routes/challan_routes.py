from flask import Blueprint, request, render_template
from app.forms.challan_form import PurchaseForm
from app.logger import logger as log

challan = Blueprint('challan', __name__)


@challan.route('/purchase', methods=['GET', 'POST'])
def purchase():
    form = PurchaseForm(request.form)

    if request.method == 'POST' and form.validate():
        # Process validated form data
        log.info(form.data)
        # Redirect or inform of successful submission, etc.
        return 'Form Submitted'

    return render_template('addentry.html', form=form)

@challan.
