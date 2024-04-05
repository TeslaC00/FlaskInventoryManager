from flask import Flask
from flask_migrate import Migrate

from app.logger import logger


# Creates flask object
def create_app(config_file='config.py'):
    app = Flask(__name__)
    # Secret Key
    app.secret_key = 'secret_key'
    # Load local configurations from config.py
    app.config.from_pyfile(config_file)
    # Initialize login manager
    from app.routes.auth import login_manager
    login_manager.init_app(app)
    # Initialize database
    from app.database import db
    db.init_app(app)
    # Create tables
    with app.app_context():
        db.create_all()
    # Initialize database migration tool
    Migrate(app, db)
    # Registering blueprints
    from app.routes import register_routes
    register_routes(app)
    return app


logger.info('Finished initializing FlaskInventoryManager')
