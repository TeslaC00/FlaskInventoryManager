from flask import Blueprint, render_template


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