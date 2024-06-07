from flask_restful import Api
from app.api.buyer_api import BuyerResource, BuyerListResource
from app.api.bill_api import BillResource, BillListResource
from app.api.challan_item_api import ChallanItemListResource, ChallanItemResource
from app.api.material_scrap_api import MaterialScrapListResource, MaterialScrapResource
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

# materials api
api.add_resource(MaterialListResource, '/api/v1/materials')
api.add_resource(MaterialResource, '/api/v1/materials/<int:part_no>')

# product materials api
api.add_resource(ProductMaterialListResource, '/api/v1/product_materials')
api.add_resource(ProductMaterialResource, '/api/v1/product_materials/<int:product_part_no>/<int:material_part_no>')

# product scraps api
api.add_resource(ProductScrapListResource, '/api/v1/product_scraps')
api.add_resource(ProductScrapResource, '/api/v1/product_scraps/<int:product_part_no>/<string:date>')

# production logs api
api.add_resource(ProductionLogListResource, '/api/v1/production_logs')
api.add_resource(ProductionLogResource, '/api/v1/production_logs/<int:production_log_id>')

# suppliers api
api.add_resource(SupplierListResource, '/api/v1/suppliers')
api.add_resource(SupplierResource, '/api/v1/suppliers/<int:supplier_id>')

# material scrap api
api.add_resource(MaterialScrapListResource, '/api/v1/material_scraps')
api.add_resource(MaterialScrapResource, '/api/v1/material_scraps/<int:material_part_no>/<string:date>')

# challan items api
api.add_resource(ChallanItemListResource, '/api/v1/challan_items')
api.add_resource(ChallanItemResource, '/api/v1/challan_items/<int:id>')
