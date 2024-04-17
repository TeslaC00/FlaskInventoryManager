# extensions.py
from flask_bcrypt import Bcrypt
from app.logger import logger
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

logger.info('Creating extensions objects')
bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()


def initialize_extensions(app):
    """Helper function to initialize all Flask extensions with the given app."""
    logger.info('Initializing extensions')

    bcrypt.init_app(app)
    logger.info('Initialized Bcrypt')

    db.init_app(app)
    logger.info('Initialized Database')

    login_manager.init_app(app)
    logger.info('Initialized Login Manager')


def create_tables(app):
    with app.app_context():
        db.create_all()
        logger.info('Database tables created (if not existing)')
