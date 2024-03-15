from flask import Blueprint, render_template
from app.models.raw_material import Raw_Material

raw_material_bp = Blueprint('raw_material_bp', __name__)


@raw_material_bp.route('/')
def show_raw_materials():
    raw_materials = Raw_Material.query.all()
    return render_template('raw_material.html', materials=raw_materials)


@raw_material_bp.route('/<unit>/')
def show_raw_material_by_unit(unit):
    raw_materials = Raw_Material.query.filter(Raw_Material.unit_type == unit).all()
    return render_template('raw_material.html', materials=raw_materials)


@raw_material_bp.route('/find/<name>/')
def show_raw_materials_by_name(name):
    pattern = f'{name}%'  # Matches anything that starts with `name`
    raw_materials = Raw_Material.query.filter(Raw_Material.raw_material_name.like(pattern)).all()
    return render_template('raw_material.html', materials=raw_materials)

