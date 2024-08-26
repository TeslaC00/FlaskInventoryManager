from flask import Blueprint, request, flash, render_template, redirect, url_for

from app.extensions import db
from app.forms.material_form import MaterialForm
from app.logger import logger
from app.models import Material

material_routes = Blueprint('material', __name__)


# "Deprecated, remove it or change if needed, usage not allowed in current state"
@material_routes.route('/api/material', methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    if form.validate_on_submit() and request.method == 'POST':
        material = Material(
            name=form.name.data,
            unit_type=form.unit_type.data,
            quantity=form.quantity.data,
        )
        db.session.add(material)
        db.session.commit()
        logger.info(f'Material {material.to_dict()} added to database')
        flash(f'Material {material.name} added to database', 'success')
        return redirect(url_for('material.add_product'))
    return render_template('material.html', form=form)


# "Deprecated, remove it or change if needed, usage not allowed in current state"
@material_routes.route('/api/materials', methods=['GET'])
def get_materials():
    logger.info(f'Fetched all materials')
    return render_template('show_materials.html')
