from app.routes.auth import auth_bp

from app.routes import form_routes
from app.routes.main_routes import main_routes
from app.routes.raw_material_routes import raw_material_bp
from app.routes.user_routes import user_bp


def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(raw_material_bp, url_prefix='/raw_materials')
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_routes)
    app.register_blueprint(form_routes)
