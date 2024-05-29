from flask_restful import Api
from app.api.buyer_api import BuyerResource, BuyerListResource
from app.api.bill_api import BillResource, BillListResource

api = Api()

# buyer api
api.add_resource(BuyerListResource, '/api/v1/buyers')
api.add_resource(BuyerResource, '/api/v1/buyers/<int:buyer_id>')

# bill api
api.add_resource(BillListResource, '/api/v1/bills')
api.add_resource(BillResource, '/api/v1/bills/<int:bill_id>')
