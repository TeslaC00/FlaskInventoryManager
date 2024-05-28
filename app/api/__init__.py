from app.extensions import api
from app.api.buyer_api import BuyerResource, BuyerListResource
from app.api.bill_api import BillResource, BillListResource

# buyer api
api.add_resource(BuyerListResource, '/api/buyers')
api.add_resource(BuyerResource, '/api/buyers/<int:buyer_id>')

# bill api
api.add_resource(BillListResource, '/api/bills')
api.add_resource(BillResource, '/api/bills/<int:bill_id>')
