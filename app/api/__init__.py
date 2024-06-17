from app.api.bill_api import bills_bp


def register_api_blueprints(api):
    api.register_blueprint(bills_bp, url_prefix='/api/v1')
