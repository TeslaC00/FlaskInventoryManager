from app.routes.auth import auth_bp
from app.routes.inventory_routes import inventory_bp
from app.routes.main_routes import main_routes


def register_routes(app):
    """
    Registers various blueprints with the Flask application.

    This function takes the Flask application instance as an argument and registers
    different blueprints for handling routes related to users, raw materials,
    authentication, the main application, forms, and inventory. Each blueprint
    encapsulates a collection of routes and optional template rendering logic
    related to a specific feature of the application.

    Parameters:
    - app: Flask application instance to which the blueprints will be registered.

    The function does not return any value. It modifies the app instance by registering
    the blueprints, which in turn adds routes to the application.

    The blueprints are registered with specific URL prefixes (where applicable) to
    organize the application's URL space. The `url_prefix` parameter is used to specify
    the starting point of the URLs for the routes included in the blueprint.

    For example, the user-related routes will start with `/users`, and the inventory-related
    routes will start with `/inventory`. Some blueprints, like `auth_bp` and `main_routes`,
    are registered without a URL prefix, meaning their routes will be accessible directly
    from the application's root URL.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_routes)
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
