from flask import Blueprint, request, flash, jsonify

from app.database import db
from app.forms.material_form import MaterialForm
from app.logger import logger
from app.models import Material

material_routes = Blueprint('material', __name__)


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


@material_routes.route('/api/materials', methods=['GET'])
def get_materials():
    materials = Material.query.all()
    logger.info(f'Fetched all materials')
    return jsonify(materials)


@material_routes.route('/api/material/<str:name>', methods=['GET'])
def get_material(name):
    material = Material.query.get(name)
    if material:
        logger.info(f'Fetched material {material.to_dict()}')
        return jsonify(material)
    else:
        logger.error(f'Material {name} not found')
        flash(f'Materia {name} not found', 'error')


@material_routes.route('/api/material/<str:name>', methods=['GET', 'POST'])
def update_material(name):
    material = Material.query.get(name)
    form = MaterialForm(obj=material)
    form.name.render_kw = {'readonly': True}
    if form.validate_on_submit() and request.method == 'POST':
        logger.info(f'Updating material {material.to_dict()}')
        form.populate_obj(material)
        db.session.commit()
        logger.info(f'Material {material.to_dict()} updated')
        flash(f'Material {material.name} updated', 'success')


@material_routes.route('/api/material/<str:name>', methods=['POST'])
def delete_material(name):
    material = Material.query.get(name)
    if material:
        db.session.delete(material)
        logger.info(f'Deleted material {material.to_dict()}')
        flash(f'Material {material.name} deleted', 'success')
    else:
        logger.error(f'Material {name} not found')
        flash(f'Material {name} not found', 'error')
