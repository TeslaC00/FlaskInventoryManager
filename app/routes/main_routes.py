# Blueprint object to define routes
from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_security import auth_required, permissions_accepted, roles_required
from sqlalchemy import text

from app.extensions import db
from app.logger import logger
from app.models import Product, Material, User

main_routes = Blueprint('main', __name__)


@main_routes.route('/base/')
@jwt_required()
def root():
    """
    Serves the base template of the application. Requires user to be logged in.

    Returns:
    - The rendered base.html template.
    """
    user_id = get_jwt_identity()
    logger.info(f'logged in user_id: {user_id}')
    return render_template('base.html')


@main_routes.route('/profile/')
# @auth_required()
def profile():
    users = User.query.all()
    for user in users:
        user.password = "REDACTED"
        user.role = ', '.join([role.name for role in user.roles])  # Convert roles to a comma-separated string
    return render_template('profile.html', users=users)


@main_routes.route('/analysis/')
# @auth_required()
def analysis():
    """
    Serves the analysis page of the application. Requires user to be logged in.

    Returns:
    - The rendered analysis.html template.
    """
    return render_template('analysis.html')


# TODO: add content to audits page
@main_routes.route('/audits/')
# @auth_required()
def audits():
    return render_template('audits.html')


# TODO: add content to settings page
@main_routes.route('/settings/')
# @auth_required()
def settings():
    return render_template('settings.html')


@main_routes.route('/addentry/')
# @auth_required()
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
