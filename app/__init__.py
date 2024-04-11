import os

from flask import Flask
from flask_migrate import Migrate

from app.logger import logger


# Creates flask object
def create_app():
    app = Flask(__name__)
    logger.info('Created Flask app object')

    # Loading environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    logger.info('Loaded Environment Variables')

    # Initialize login manager
    from app.routes.auth import login_manager
    login_manager.init_app(app)
    logger.info('Initialized login manager')

    # Initialize database
    from app.database import db
    db.init_app(app)
    logger.info('Initialized database')
    # Create tables
    # with app.app_context():
    #     db.create_all()

    # Initialize database migration tool
    Migrate(app, db)
    logger.info('Initialized flask migrate')

    # Registering blueprints
    from app.routes import register_routes
    register_routes(app)
    logger.info('Registered routes')

    logger.info('Finished initializing FlaskInventoryManager')
    return app
