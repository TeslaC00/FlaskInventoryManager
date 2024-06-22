import os

from dotenv import load_dotenv
from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security

from app.converters import DateConverter
from app.extensions import initialize_extensions, db
from app.logger import logger
from instance.config import APIConfig


def create_app():
    # Creates flask object
    app = Flask(__name__, instance_relative_config=True)
    logger.info('Created Flask app object')

    app.url_map.converters['date'] = DateConverter

    load_dotenv()
    app.config.from_object(APIConfig)
    logger.info('Loaded Api configurations')
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

    logger.info(app.config['FLASK_ENV'])
    logger.info(app.config['SECRET_KEY'])
    logger.info(app.config['SECURITY_PASSWORD_SALT'])
    logger.info(app.config['SQLALCHEMY_DATABASE_URI'])
    logger.info(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
    logger.info(app.config['REMEMBER_COOKIE_SAMESITE'])
    logger.info(app.config['SESSION_COOKIE_SAMESITE'])
    logger.info(app.config['DEBUG'])
    # logger.info(app.config['FLASK_DEBUG'])

    initialize_extensions(app)
    logger.info('All extensions initialized')

    init_security(app)

    create_tables(app)
    logger.info('All tables created')

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


def init_security(app):
    print(f"SECRET_KEY in app config: {app.config['SECRET_KEY']}")
    from app.models.user import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
