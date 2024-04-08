from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for

from app.forms.supplier_form import SupplierForm
from app.logger import logger
from app.models import Supplier

supplier_routes = Blueprint('supplier', __name__)


@supplier_routes.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify(suppliers)


@supplier_routes.route('/api/supplier', methods=['POST', 'GET'])
def add_supplier():
    form = SupplierForm()
    message = None
    if request.method == 'POST' and form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data, GST_No=form.GST_No.data,
            state_code=form.state_code.data, state_name=form.state_name.data)
        logger.info(f'Added supplier {supplier.to_dict()} to supplier table')
        flash('New Supplier Added', 'success')
        return redirect(url_for('supplier.add_supplier'))
    return render_template('add_supplier.html', form=form)
