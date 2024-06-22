import os

from dotenv import load_dotenv
from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security

from app.converters import DateConverter
from app.extensions import initialize_extensions, db
from app.logger import logger


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

    init_security(app)
    create_tables(app)

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
        app.security.datastore.find_or_create_role(
            name="user", permissions={"user-read", "user-write"}
        )
        db.session.commit()
        if not app.security.datastore.find_user(email="user@gmail.com"):
            from flask_security import hash_password
            app.security.datastore.create_user(email="user@gmail.com",
                                               password=hash_password("password"), roles=["user"])
        db.session.commit()


def init_security(app):
    from app.models.user import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
    logger.info('Initialized security')
