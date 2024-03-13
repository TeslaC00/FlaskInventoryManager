from flask import Flask
from flask_migrate import Migrate

from .database import db
from .routes import main_routes

9
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
    app.register_blueprint(main_routes)

    return app
