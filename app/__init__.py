import os

from dotenv import load_dotenv
from flask import Flask

from app.converters import DateConverter
from app.extensions import initialize_extensions
from app.logger import logger
from app.security import init_security
from app.extensions import db


def create_app():
    # Creates flask object
    app = Flask(__name__, instance_relative_config=True)
    logger.info('Created Flask app object')

    app.url_map.converters['date'] = DateConverter

    load_dotenv()
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'development':
        from instance.config import DevelopmentConfig as ConfigClass
    elif env == 'testing':
        from instance.config import TestingConfig as ConfigClass
    elif env == 'production':
        from instance.config import ProductionConfig as ConfigClass
    else:
        raise ValueError(f"Unknown environment: {env}")

    app.config.from_object(ConfigClass)

    app.config['FLASK_ENV'] = env
    # Configure Flask-Security-Too to use 'username' instead of 'email'
    # app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = 'username'

    logger.debug(app.config['FLASK_ENV'])
    logger.debug(app.config['SECRET_KEY'])
    logger.debug(app.config['SECURITY_PASSWORD_SALT'])
    logger.debug(app.config['SQLALCHEMY_DATABASE_URI'])
    logger.debug(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
    logger.debug(app.config['REMEMBER_COOKIE_SAMESITE'])
    logger.debug(app.config['SESSION_COOKIE_SAMESITE'])
    logger.debug(app.config['DEBUG'])

    initialize_extensions(app)
    logger.info('All extensions initialized')

    create_tables(app)
    init_security(app)

    # Registering blueprints
    from app.routes import register_routes
    register_routes(app)
    logger.info('Registered routes')

    logger.info('Finished initializing FlaskInventoryManager')
    return app


def create_tables(app):
    with app.app_context():
        db.create_all()
        logger.info('Database tables created (if not existing)')
