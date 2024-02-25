from flask import Flask
from .routes import main_routes


def create_app():
    # Creates flask object
    app = Flask(__name__)
    # Registering blueprints
    app.register_blueprint(main_routes)
    return app
