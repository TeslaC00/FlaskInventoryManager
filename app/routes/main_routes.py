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
    return render_template('base.html')


@main_routes.route('/index/')
@login_required
def index():
    all_tables = db.metadata.tables.keys()
    items = ["Item", "Item", "Item", "Item", "Item", "Item", "Item", "Item", "Item", "Item", "Item2", "Item", "Item",
             "Item", "Item", "Item", "Item", "Item"]
    return render_template('index.html', all_tables=all_tables, items=items)


@main_routes.route('/analysis/')
@login_required
def analysis():
    return render_template('analysis.html')


@main_routes.route('/orders/')
@login_required
def orders():
    return render_template('orders.html')


@main_routes.route('/form')
def form():
    return render_template('form.html')


@main_routes.route('/test_database_connection/')
def test_database_connection():
    try:
        # Execute a simple query to test the connection
        db.session.execute(text('SELECT 1'))
        return 'Database connected successfully!'
    except Exception as e:
        return f'Database connection error: {str(e)}'


# This function retrieves all the tables in the database
def get_all_tables():
    meta = db.metadata
    return meta.tables.keys()


@main_routes.route('/show_tables/')
def show_tables():
    all_tables = get_all_tables()
    return render_template('show_tables.html', tables=all_tables)


@main_routes.route('/spreadsheet/')
def show_tables2():
    records = Raw_Material_Records.query.all()
    results = [record.to_dict() for record in records]
    return render_template('spreadsheet.html', tables=results)


# This function retrieves all the tables in the database and returns in a list
def get_all_tables_list():
    meta = db.metadata
    db.reflect()
    return list(meta.tables.keys())


@main_routes.route('/update-data/', methods=['POST'])
def update_data():
    changes = request.json.get('changes', [])
    # Process your changes here (e.g., update your database)
    for change in changes:
        row, prop, oldVal, newVal = change
        print(f"Row {row} column {prop} changed from {oldVal} to {newVal}")
        # Update the database based on each change

    return jsonify({"status": "success"})


@main_routes.route('/json')
def json_response():
    records = Raw_Material_Records.query.all()
    results = [record.to_dict() for record in records]
    return jsonify(results)
