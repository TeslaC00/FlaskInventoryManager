from flask import Flask
from flask_migrate import Migrate

from app.routes import register_routes
from .database import db

# Creates flask object
app = Flask(__name__)

# Load local configurations from config.py
app.config.from_pyfile('config.py')

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Initialize database migration tool
Migrate(app, db)

# Registering blueprints
register_routes(app)
