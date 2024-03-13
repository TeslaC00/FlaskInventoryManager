from flask import Blueprint, render_template
from sqlalchemy import text
from .database import db

# Blueprint object to define routes
main_routes = Blueprint('main', __name__)


@main_routes.route('/')
def root():
    return render_template('home.html')


@main_routes.route('/index/')
def index():
    return render_template('index.html')


@main_routes.route('/analysis/')
def analysis():
    return render_template('analysis.html')


@main_routes.route('/orders/')
def orders():
    return render_template('orders.html')

@main_routes.route('/test_database_connection')
def test_database_connection():
    try:
        # Execute a simple query to test the connection
        db.session.execute(text('SELECT 1'))
        return 'Database connected successfully!'
    except Exception as e:
        return f'Database connection error: {str(e)}'