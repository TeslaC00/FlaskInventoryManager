from flask_restful import Api
from app.api.buyer_api import BuyerResource, BuyerListResource
from app.api.bill_api import BillResource, BillListResource
from app.api.materials_api import MaterialListResource, MaterialResource
from app.api.product_material_api import ProductMaterialListResource, ProductMaterialResource
from app.api.product_scrap_api import ProductScrapListResource, ProductScrapResource
from app.api.productionlog_api import ProductionLogListResource, ProductionLogResource
from app.api.supplier_api import SupplierListResource, SupplierResource

api = Api()

# buyer api
api.add_resource(BuyerListResource, '/api/v1/buyers')
api.add_resource(BuyerResource, '/api/v1/buyers/<int:buyer_id>')

# bill api
api.add_resource(BillListResource, '/api/v1/bills')
api.add_resource(BillResource, '/api/v1/bills/<int:bill_id>')

api.add_resource(MaterialListResource, '/materials')
api.add_resource(MaterialResource, '/materials/<int:part_no>')

api.add_resource(ProductMaterialListResource, '/product_materials')
api.add_resource(ProductMaterialResource, '/product_materials/<int:product_part_no>/<int:material_part_no>')

api.add_resource(ProductScrapListResource, '/product_scraps')
api.add_resource(ProductScrapResource, '/product_scraps/<int:product_part_no>/<string:date>')

api.add_resource(ProductionLogListResource, '/production_logs')
api.add_resource(ProductionLogResource, '/production_logs/<int:production_log_id>')

api.add_resource(SupplierListResource, '/suppliers')
api.add_resource(SupplierResource, '/suppliers/<int:supplier_id>')
