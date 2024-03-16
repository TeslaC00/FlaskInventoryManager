from flask import Flask
from flask_migrate import Migrate

from .database import db
from .routes import main_routes
from .routes.user_routes import user_bp
from app.routes import register_routes


def create_app():
    # Creates flask object
    app = Flask(__name__)

    # Load local configurations from config.py
    app.config.from_pyfile('config.py')

    # Initialize database
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    # Initialize database migration tool
    migrate = Migrate(app, db)

    # Registering blueprints
    register_routes(app)

    return app
