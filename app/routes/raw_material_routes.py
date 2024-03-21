from flask import Blueprint, render_template

from app.models.raw_material import Raw_Material

raw_material_bp = Blueprint('raw_material_bp', __name__)


@raw_material_bp.route('/')
def show_raw_materials():
    """
    Route to display a list of all raw materials.

    Fetches all raw material records from the database and renders them on the 'raw_material.html' template.

    Returns:
        Rendered template ('raw_material.html') with all raw materials passed as context.
    """
    raw_materials = Raw_Material.query.all()
    return render_template('raw_material.html', materials=raw_materials)


@raw_material_bp.route('/<unit>/')
def show_raw_material_by_unit(unit):
    """
    Route to display raw materials filtered by their unit type.

    Parameters:
        unit (str): The unit type by which to filter the raw materials.

    Fetches raw material records from the database that match the specified unit type and renders them on the
    'raw_material.html' template.

    Returns:
        Rendered template ('raw_material.html') with filtered raw materials passed as context.
    """
    raw_materials = Raw_Material.query.filter(Raw_Material.unit_type == unit).all()
    return render_template('raw_material.html', materials=raw_materials)


@raw_material_bp.route('/find/<name>/')
def show_raw_materials_by_name(name):
    """
    Route to display raw materials filtered by name.

    Parameters:
        name (str): The name or beginning of the name to filter the raw materials by.

    Uses a pattern matching to fetch raw material records that start with the specified name from the database.
    Renders these filtered records on the 'raw_material.html' template.

    Returns:
        Rendered template ('raw_material.html') with raw materials that match the pattern passed as context.
    """
    pattern = f'{name}%'  # Matches anything that starts with `name`
    raw_materials = Raw_Material.query.filter(Raw_Material.raw_material_name.like(pattern)).all()
    return render_template('raw_material.html', materials=raw_materials)
