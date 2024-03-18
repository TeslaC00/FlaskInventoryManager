from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from app.routes import register_routes
from .database import db
from .routes.auth import login_manager

# Creates flask object
app = Flask(__name__)

# Secret Key
app.secret_key = 'secret_key'

# Load local configurations from config.py
app.config.from_pyfile('config.py')

# Initialize login manager
login_manager.init_app(app)

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Initialize database migration tool
Migrate(app, db)

# Registering blueprints
register_routes(app)
