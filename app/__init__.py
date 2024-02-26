from flask import Flask
from .database import db

from .routes import main_routes


def create_app():
    # Creates flask object
    app = Flask(__name__)

    # Load local configurations from config.py
    app.config.from_pyfile('config.py')

    # Initialize database
    db.init_app(app)

    # Registering blueprints
    app.register_blueprint(main_routes)

    return app
