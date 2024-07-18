from flask import render_template, Blueprint

from app.logger import logger
from app.models import Product, Material

# Initialize a Blueprint for inventory-related routes
inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inv_raw/')
def show_inv_raw():
    """
    Route to display the inventory page, showing tables for both raw materials and produced goods.
    Fetches data from the database for raw materials and goods, converting them to dictionaries for easy rendering in templates.

    :return: Rendered 'inv_raw.html' template with raw material and produced goods data passed as context.
    """
    try:
        return render_template('inv_raw.html',)
    except Exception as e:
        # TODO: add error page to show errors
        logger.error('An error occurred', e)
        # return render_template('#error template')
        return e.__str__()


@inventory_bp.route('/inv_produced/')
def show_inv_prod():
    """
    Route to display the inventory page, showing tables for both raw materials and produced goods.
    Fetches data from the database for raw materials and goods, converting them to dictionaries for easy rendering in templates.

    :return: Rendered 'inv_prod.html' template with raw material and produced goods data passed as context.
    """
    try:
        return render_template('inv_prod.html')
    except Exception as e:
        # TODO: add error page to show errors
        logger.error('An error occurred', e)
        # return render_template('#error template')
        return 'Something went wrong'
