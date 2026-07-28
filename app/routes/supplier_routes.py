from flask import Blueprint, request, render_template, flash, redirect, url_for

from app.extensions import db
from app.forms.supplier_form import SupplierForm
from app.logger import logger
from app.models import Supplier

supplier_routes = Blueprint('supplier', __name__)


# "Deprecated, remove it or change if needed, usage not allowed in current state"
@supplier_routes.route('/api/supplier', methods=['POST', 'GET'])
def add_supplier():
    form = SupplierForm()
    if request.method == 'POST' and form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data, GST_No=form.GST_No.data,
            state_code=form.state_code.data, state_name=form.state_name.data)
        db.session.add(supplier)
        db.session.commit()
        logger.info(f'Added supplier {supplier.to_dict()} to supplier table')
        flash(f'New Supplier {supplier.name} Added', 'success')
        return redirect(url_for('supplier.add_supplier'))
    return render_template('add_supplier.html', form=form)


# "Deprecated, remove it or change if needed, usage not allowed in current state"
@supplier_routes.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    logger.info('Fetched all suppliers')
    return render_template('show_suppliers.html', suppliers=suppliers)
    # return jsonify(suppliers)
