from flask import render_template, Blueprint

from app.logger import logger
from app.models import Goods, Raw_Material

# Initialize a Blueprint for inventory-related routes
inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/')
def show_inventory():
    """
    Route to display the inventory page, showing tables for both raw materials and produced goods.
    Fetches data from the database for raw materials and goods, converting them to dictionaries for easy rendering in templates.

    :return: Rendered 'inventory.html' template with raw material and produced goods data passed as context.
    """
    try:
        # Query all raw material records from the database
        raw_material_data = Raw_Material.query.all()
        # Query all produced goods records from the database
        produced_good_data = Goods.query.all()

        # Convert the raw material and produced goods records to dictionaries for template rendering
        # Assuming 'to_dict' method is implemented in both 'Raw_Material' and 'Goods' models for serialization
        table1 = [record.to_dict() for record in raw_material_data]
        table2 = [record.to_dict() for record in produced_good_data]

        logger.info('Queried Raw Material and Goods table from database')
        # Render the 'inventory.html' template, passing the raw material and produced goods data for display
        return render_template('inventory.html', table1=table1, table2=table2)
    except Exception as e:
        # TODO: add error page to show errors
        logger.error('An error occurred', e)
        # return render_template('#error template')
        return 'Something went wrong'
