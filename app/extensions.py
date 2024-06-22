# extensions.py
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.logger import logger

logger.info('Creating extensions objects')
db = SQLAlchemy()
login_manager = LoginManager()
api = Api()


def initialize_extensions(app):
    """Helper function to initialize all Flask extensions with the given app."""

    db.init_app(app)
    logger.debug('Initialized Database')

    login_manager.init_app(app)
    logger.debug('Initialized Login Manager')

    logger.debug('Initialized Api')
    api.init_app(app)
    from app.api import register_api_blueprints
    register_api_blueprints(api)

    logger.info('Initialized extensions')
