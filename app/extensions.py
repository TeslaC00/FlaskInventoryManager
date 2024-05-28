# extensions.py
from flask_bcrypt import Bcrypt
from app.logger import logger
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api

logger.info('Creating extensions objects')
bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
api = Api()


def initialize_extensions(app):
    """Helper function to initialize all Flask extensions with the given app."""
    logger.info('Initializing extensions')

    bcrypt.init_app(app)
    logger.info('Initialized Bcrypt')

    db.init_app(app)
    logger.info('Initialized Database')

    login_manager.init_app(app)
    logger.info('Initialized Login Manager')

    api.init_app(app)
    logger.info('Initialized Flask Restful API')
