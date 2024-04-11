from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for

from app.database import db
from app.forms.supplier_form import SupplierForm
from app.logger import logger
from app.models import Supplier

supplier_routes = Blueprint('supplier', __name__)


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


@supplier_routes.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    logger.info('Fetched all suppliers')
    return render_template('show_suppliers.html', suppliers=suppliers)
    # return jsonify(suppliers)


@supplier_routes.route('/api/supplier/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if supplier:
        logger.info(f'Fetched supplier {supplier.to_dict()}')
        return jsonify(supplier)
    else:
        logger.error(f'Supplier {supplier_id} not found')
        flash('Supplier not found', 'error')


@supplier_routes.route('/api/supplier/<int:supplier_id>', methods=['GET', 'POST'])
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)  # 404 -> object not found
    form = SupplierForm(obj=supplier)
    if form.validate_on_submit() and request.method == 'POST':
        logger.info(f'Updating supplier {supplier.to_dict()}')
        form.populate_obj(supplier)
        db.session.commit()
        logger.info(f'Updated supplier {supplier.to_dict()}')
        flash('Updated Supplier', 'success')


@supplier_routes.route('/api/supplier/<int:supplier_id>', methods=['POST'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if supplier:
        db.session.delete(supplier)
        db.session.commit()
        logger.info(f'Deleted supplier {supplier.to_dict()}')
        flash(f'Supplier Deleted', 'success')
    else:
        logger.error(f'Supplier {supplier_id} not found')
        flash(f'Supplier {supplier_id} Not Found', 'error')
