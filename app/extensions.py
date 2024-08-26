# extensions.py
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.logger import logger

logger.info('Creating extensions objects')
db = SQLAlchemy()
api = Api()
jwt = JWTManager()


def initialize_extensions(app):
    """Helper function to initialize all Flask extensions with the given app."""

    db.init_app(app)
    logger.debug('Initialized Database')

    jwt.init_app(app)
    logger.debug('Initialized JWT')

    api.init_app(app)
    logger.debug('Initialized Api')
    from app.api import register_api_blueprints
    register_api_blueprints(api)

    logger.info('Initialized extensions')
