# Blueprint object to define routes
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import text
from typing_extensions import deprecated

from app.extensions import db
from app.models import Product, Material, User

main_routes = Blueprint('main', __name__)


@main_routes.route('/base/')
# @login_required
def root():
    """
    Serves the base template of the application. Requires user to be logged in.

    Returns:
    - The rendered base.html template.
    """
    return render_template('base.html')


@main_routes.route('/profile/')
# @login_required
def profile():
    users = User.query.all()
    return render_template('profile.html', users=users)


@main_routes.route('/analysis/')
# @login_required
def analysis():
    """
    Serves the analysis page of the application. Requires user to be logged in.

    Returns:
    - The rendered analysis.html template.
    """
    return render_template('analysis.html')

# @deprecated(1)
# @main_routes.route('/orders/')
# @login_required
# def orders():
#     """
#     Serves the orders page of the application. Requires user to be logged in.
#
#     Returns:
#     - The rendered orders.html template.
#     """
#     return render_template('orders.html')


# TODO: add content to audits page
@main_routes.route('/audits/')
# @login_required
def audits():
    return render_template('audits.html')


# TODO: add content to settings page
@main_routes.route('/settings/')
# @login_required
def settings():
    return render_template('settings.html')


@main_routes.route('/addentry/')
# @login_required
def addentry():
    return render_template('addentry.html')



@main_routes.route('/test_database_connection/')
def test_database_connection():
    """
    Tests the database connection by executing a simple SELECT query.

    Returns:
    - A success message if the connection is successful.
    - An error message detailing the issue if the connection fails.
    """
    try:
        db.session.execute(text('SELECT 1'))
        return 'Database connected successfully!'
    except Exception as e:
        return f'Database connection error: {str(e)}'


@main_routes.route('/update-data/', methods=['POST'])
def update_data():
    """
    Receives a JSON payload with data changes and processes these changes (e.g., updating the database).

    Returns:
    - A JSON response indicating the success of the update operation.
    """
    changes = request.json.get('changes', [])
    for change in changes:
        row, prop, oldVal, newVal = change
        print(f"Row {row} column {prop} changed from {oldVal} to {newVal}")
        # Update the database based on each change

    return jsonify({"status": "success"})


# TODO: change from records to production log
# @main_routes.route('/json')
# def json_response():
#     """
#     Retrieves all records from the Raw_Material_Records table and returns them in a JSON format.
#
#     Returns:
#     - A JSON response containing all records from Raw_Material_Records.
#     """
#     records = Raw_Material_Records.query.all()
#     results = [record.to_dict() for record in records]
#     return jsonify(results)


@main_routes.route('/autocomplete', methods=['GET'])
def autocomplete():
    """
    Route to handle autocomplete suggestions.
    Fetches goods names from the database that match the user's search query and returns them in a JSON format suitable
    for autocomplete functionalities.

    :return: A JSON response containing matching results, each with an "id" and "name" derived from goods names in the
    database.
    """
    search = request.args.get('q')  # Get the search query parameter 'q' from the URL
    results = Product.query.filter(Product.name.like(f'%{search}%')).limit(
        10).all()  # Query the database for goods names that contain the search term
    # Prepare and return the JSON response with the search results
    return jsonify(matching_results=[{"name": item.name} for item in results])


@main_routes.route('/autocomplete_raw', methods=['GET'])
def autocomplete_raw():
    """
    Route to handle autocomplete suggestions.
    Fetches raw material names from the database that match the user's search query and returns them in a JSON format suitable
    for autocomplete functionalities.

    :return: A JSON response containing matching results, each with an "id" and "name" derived from raw material names in the
    database.
    """
    search = request.args.get('q')  # Get the search query parameter 'q' from the URL
    results = Material.query.filter(Material.name.like(f'%{search}%')).limit(
        10).all()  # Query the database for goods names that contain the search term
    # Prepare and return the JSON response with the search results
    return jsonify(matching_results=[{"name": raw.item_name} for raw in results])
