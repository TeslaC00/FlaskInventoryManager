from app.extensions import api
from app.api.buyer_api import BuyerResource, BuyerListResource

# buyer api
api.add_resource(BuyerListResource, '/api/buyers')
api.add_resource(BuyerListResource, '/api/buyers/<int:buyer_id>')
