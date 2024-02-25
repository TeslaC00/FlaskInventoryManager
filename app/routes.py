from flask import Blueprint, render_template


# Blueprint object to define routes
main_routes = Blueprint('main', __name__)


@main_routes.route('/')
def root():
    return 'Welcome to Inventory Management System!'


@main_routes.route('/index/')
def index():
    return render_template('index.html')
