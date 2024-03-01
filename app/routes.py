from flask import Blueprint, render_template
from sqlalchemy import text
from .database import db
from .models import User

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

# This function retrieves all the tables in the database
def get_all_tables():
    meta = db.metadata
    return meta.tables.keys()

@main_routes.route('/show_tables')
def show_tables():
    all_tables = get_all_tables()
    return render_template('show_tables.html', tables=all_tables)

# Create a route to add values to the table
@main_routes.route('/add_user/<username>')
def add_user(username):
    new_user = User(username=username, email=username)
    db.session.add(new_user)
    db.session.commit()
    return 'User added successfully'

@main_routes.route('/users')
def show_users():
    # Fetch all users from the User table
    users = User.query.all()
    return render_template('user.html', users=users)
