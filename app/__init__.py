import os

from flask import Flask

from app.logger import logger
from app.extensions import initialize_extensions, create_tables


def create_app():
    # Creates flask object
    app = Flask(__name__)
    logger.info('Created Flask app object')

    # Loading environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    logger.info('Loaded Environment Variables')

    initialize_extensions(app)
    logger.info('All extensions initialized')

    create_tables(app)
    logger.info('All tables created with seed')

    # Registering blueprints
    from app.routes import register_routes
    register_routes(app)
    logger.info('Registered routes')

    logger.info('Finished initializing FlaskInventoryManager')
    return app
