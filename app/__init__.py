import os

from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security

from app.logger import logger
from app.extensions import initialize_extensions, db


def create_app():
    # Creates flask object
    app = Flask(__name__)
    logger.info('Created Flask app object')

    # Loading environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    # what ?
    # have session and remember cookie be samesite (flask/flask_login)
    app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
    app.config["SESSION_COOKIE_SAMESITE"] = "strict"
    logger.info('Loaded Environment Variables')

    initialize_extensions(app)
    logger.info('All extensions initialized')

    init_security(app)

    create_tables(app)
    logger.info('All tables created with seed')

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
    from app.models.user import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
