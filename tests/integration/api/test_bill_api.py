# def test_create_user(client):
#     response = client.post('/users', json={"username": "john", "password": "password"})
#     assert response.status_code == 201
#
# def test_login_success(client):
#     client.post('/users', json={"username": "john", "password": "password"})
#     response = client.post('/login', json={"username": "john", "password": "password"})
#     assert response.status_code == 200
#
# def test_login_invalid_user(client):
#     response = client.post('/login', json={"username": "invalid", "password": "password"})
#     assert response.status_code == 401
from app.models import Product, Unit

api_url_prefix = '/api/v1/'


# def test_create_bill_item(client):
#     response = client.post(api_url_prefix + 'bill_item', json={})
#     assert response.status_code == 201

def test_create_bill(client, session):
    unit = Unit(name='test_unit')
    session.add(unit)
    session.commit()

    product = Product()
    product.name = 'test_product'
    product.unit_id = unit.id
    product.quantity = 10
    product.price = 100
    product.c_gst = 0.1
    product.i_gst = 0.2
    product.s_gst = 0.3
    session.add(product)
    session.commit()

    response = client.post('/api/v1/bills',
                           json={'buyer_id': 1, 'total_price': 1, 'date': '2024-09-19',
                                 'purchase_order': 'string',
                                 'remarks': 'remark',
                                 'items': [
                                     {
                                         "quantity": 0,
                                         "price": 0,
                                         "c_gst": 0,
                                         "s_gst": 0,
                                         "i_gst": 0,
                                         "product_part_no": product.part_no
                                     }
                                 ]})
    assert response.status_code == 201
