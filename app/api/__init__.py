from app.api.bill_api import bills_bp
from .bill_item_api import bill_item_bp
from .audit_log_api import audit_log_bp
from .buyer_api import buyer_bp
from .challan_api import challan_bp
from .challan_item_api import challan_item_bp
from .supplier_api import supplier_bp
from .material_api import material_bp
from .material_scrap_api import material_scrap_bp
from .product_api import product_bp
from .product_material_api import product_material_bp
from .product_scrap_api import product_scrap_bp
from .production_log_api import production_log_bp
from .unit_api import unit_bp
from .user_api import user_bp


def register_api_blueprints(api):
    api.register_blueprint(bills_bp, url_prefix='/api/v1')
    api.register_blueprint(bill_item_bp, url_prefix='/api/v1')
    api.register_blueprint(audit_log_bp, url_prefix='/api/v1')
    api.register_blueprint(buyer_bp, url_prefix='/api/v1')
    api.register_blueprint(challan_bp, url_prefix='/api/v1')
    api.register_blueprint(challan_item_bp, url_prefix='/api/v1')
    api.register_blueprint(supplier_bp, url_prefix='/api/v1')
    api.register_blueprint(material_bp, url_prefix='/api/v1')
    api.register_blueprint(material_scrap_bp, url_prefix='/api/v1')
    api.register_blueprint(product_bp, url_prefix='/api/v1')
    api.register_blueprint(product_material_bp, url_prefix='/api/v1')
    api.register_blueprint(product_scrap_bp, url_prefix='/api/v1')
    api.register_blueprint(production_log_bp, url_prefix='/api/v1')
    api.register_blueprint(unit_bp, url_prefix='/api/v1')
    api.register_blueprint(user_bp, url_prefix='/api/v1')
