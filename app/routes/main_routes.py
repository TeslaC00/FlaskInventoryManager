# Blueprint object to define routes
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import text

from app.database import db
from app.models import Raw_Material_Records

main_routes = Blueprint('main', __name__)


@main_routes.route('/base/')
@login_required
def root():
    """
    Serves the base template of the application. Requires user to be logged in.

    Returns:
    - The rendered base.html template.
    """
    return render_template('base.html')


@main_routes.route('/index/')
@login_required
def index():
    """
    Serves the index page with a list of database tables and pre-defined items. Requires user to be logged in.

    Returns:
    - The rendered index.html template with a list of all database tables and items.
    """
    all_tables = db.metadata.tables.keys()
    items = ["Item"] * 17 + ["Item2"]
    return render_template('index.html', all_tables=all_tables, items=items)


@main_routes.route('/analysis/')
@login_required
def analysis():
    """
    Serves the analysis page of the application. Requires user to be logged in.

    Returns:
    - The rendered analysis.html template.
    """
    return render_template('analysis.html')


@main_routes.route('/orders/')
@login_required
def orders():
    """
    Serves the orders page of the application. Requires user to be logged in.

    Returns:
    - The rendered orders.html template.
    """
    return render_template('orders.html')


@main_routes.route('/form')
def form():
    """
    Serves a generic form page.

    Returns:
    - The rendered form.html template.
    """
    return render_template('form.html')


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


@main_routes.route('/show_tables/')
def show_tables():
    """
    Retrieves and displays all the tables in the database.

    Returns:
    - The rendered show_tables.html template with a list of all database tables.
    """
    all_tables = get_all_tables()
    return render_template('show_tables.html', tables=all_tables)


@main_routes.route('/spreadsheet/')
def show_tables2():
    """
    Retrieves all records from the Raw_Material_Records table and displays them in a spreadsheet format.

    Returns:
    - The rendered spreadsheet.html template with all records from Raw_Material_Records.
    """
    records = Raw_Material_Records.query.all()
    results = [record.to_dict() for record in records]
    return render_template('spreadsheet.html', tables=results)


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


@main_routes.route('/json')
def json_response():
    """
    Retrieves all records from the Raw_Material_Records table and returns them in a JSON format.

    Returns:
    - A JSON response containing all records from Raw_Material_Records.
    """
    records = Raw_Material_Records.query.all()
    results = [record.to_dict() for record in records]
    return jsonify(results)
