from datetime import date

from app.models import Product, Unit, Bill, Buyer, IndianState


def test_get_bills_without_filters(client, session):
    # Given: Two bills in the database
    state = IndianState(name='State', abbreviation='S')
    session.add(state)
    session.commit()

    buyer = Buyer(GST_No='123456789012345', name='buyer', state_code=state.id, address='address')
    session.add(buyer)
    session.commit()

    bill_1 = Bill(buyer_id=buyer.id, total_price=10, date=date.today(), purchase_order='order', remarks='remarks')
    bill_2 = Bill(buyer_id=buyer.id, total_price=10, date=date.today(), purchase_order='order', remarks='remarks')
    session.add(bill_1)
    session.add(bill_2)
    session.commit()

    # When: get bills API is called
    response = client.get('/api/v1/bills')

    # Then: The response should have status code 200 and valid data with fields
    assert response.status_code == 200
    print(response.json)
    assert len(response.json) == 2
    json_ = response.json[0]
    assert 'bill_items' in json_
    assert 'buyer' in json_
    assert 'id' in json_
    assert 'total_price' in json_
    assert 'date' in json_
    assert 'purchase_order' in json_
    assert 'remarks' in json_
    assert json_['total_price'] == 10
    assert json_['date'] == date.today().__str__()
    assert json_['purchase_order'] == 'order'
    assert json_['remarks'] == 'remarks'
    assert json_['buyer']['id'] == buyer.id
    assert json_['bill_items'] == []


def test_get_bills_with_filters(client, session):
    # Given: Two bills in the database
    state = IndianState(name='State', abbreviation='S')
    session.add(state)
    session.commit()

    buyer = Buyer(GST_No='123456789012345', name='buyer', state_code=state.id, address='address')
    session.add(buyer)
    session.commit()

    bill_1 = Bill(buyer_id=buyer.id, total_price=10, date=date.today(), purchase_order='order1', remarks='remarks1')
    bill_2 = Bill(buyer_id=buyer.id, total_price=1, date=date.today(), purchase_order='order2', remarks='remarks2')
    bill_3 = Bill(buyer_id=buyer.id, total_price=100, date=date.today(), purchase_order='order3', remarks='remarks3')
    session.add(bill_1)
    session.add(bill_2)
    session.add(bill_3)
    session.commit()

    # When: get bills API is called with filters
    response = client.get('/api/v1/bills?buyer_id=1&search=order3')

    # Then: The response should have status code 200 with filtered bills
    assert response.status_code == 200
    assert len(response.json) == 1
    json_ = response.json[0]
    assert 'bill_items' in json_
    assert 'buyer' in json_
    assert 'id' in json_
    assert 'total_price' in json_
    assert 'date' in json_
    assert 'purchase_order' in json_
    assert 'remarks' in json_
    assert json_['total_price'] == 100
    assert json_['date'] == date.today().__str__()
    assert json_['purchase_order'] == 'order3'
    assert json_['remarks'] == 'remarks3'
    assert json_['buyer']['id'] == buyer.id
    assert json_['bill_items'] == []


def test_get_bills_no_result(client):
    # Given: No bill in the database
    # When: get bills API is called
    response = client.get('/api/v1/bills')

    # Then: the response should have status code 200 and len 0
    assert response.status_code == 200
    assert response.json == []


def test_get_bills_invalid_filters(client):
    # Given: Bills in the database
    # When: get bills API is called with invalid filters
    response = client.get('/api/v1/bills?buyer_id=number')

    # Then: the response should have status code 400
    assert response.status_code == 422


def test_create_bill(client, session):
    # Given: A unit and a product are created in the database
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

    # When: A request is made to create a new bill with valid data
    valid_data = {'buyer_id': 1, 'total_price': 1, 'date': '2024-09-19',
                  'purchase_order': 'string',
                  'remarks': 'remarks',
                  'items': [
                      {
                          "quantity": 1,
                          "price": 10,
                          "c_gst": 0.1,
                          "s_gst": 0.2,
                          "i_gst": 0.3,
                          "product_part_no": product.part_no
                      }
                  ]}
    response = client.post('/api/v1/bills', json=valid_data)

    # Then: The response should have a status code of 201 and contain the necessary fields
    assert response.status_code == 201
    assert 'buyer_id' in response.json
    assert 'total_price' in response.json
    assert 'date' in response.json
    assert 'purchase_order' in response.json
    assert 'remarks' in response.json
    assert response.json['total_price'] == 16


def test_create_bill_missing_required_fields(client):
    # Given: A request is sent with missing required fields
    # When: The API is called with insufficient data
    response = client.post('/api/v1/bills', json={'total_price': 100})

    # Then: The response should fail with a status code of 422
    assert response.status_code == 422
    json_ = response.json['errors']['json']
    assert 'buyer_id' in json_
    assert 'date' in json_
    assert 'items' in json_
    assert 'purchase_order' in json_
    assert json_['buyer_id'] == ['Missing data for required field.']
    assert json_['date'] == ['Missing data for required field.']
    assert json_['purchase_order'] == ['Missing data for required field.']
    assert json_['items'] == ['Missing data for required field.']


def test_create_bill_improper_params(client):
    # Given: A bill with improper data is prepared
    # When: The data is sent to create a new bill
    invalid_data = {'buyer_id': 0, 'total_price': 0, 'date': '2024/09/19',
                    'purchase_order': 'abcdefghijklmnopqrstuvwxyz0123456789', 'items': []}
    response = client.post('/api/v1/bills', json=invalid_data)

    # Then: The response should fail with a status code of 422
    assert response.status_code == 422
    json_ = response.json['errors']['json']
    assert 'buyer_id' in json_
    assert 'date' in json_
    assert 'purchase_order' in json_
    # assert 'items' in json_


def test_create_bill_invalid_json(client):
    # Given: Invalid JSON data is prepared
    # When: A request is sent to create a bill with invalid JSON
    response = client.post('/api/v1/bills', data='invalid_json', content_type='application/json')

    # Then: The response should have a status code of 400 for invalid JSON
    assert response.status_code == 400
    assert "Invalid JSON" in response.data.decode()


def test_put_bill(client, session):
    # Given: Two bills in the database
    state = IndianState(name='State', abbreviation='S')
    session.add(state)
    session.commit()

    buyer = Buyer(GST_No='123456789012345', name='buyer', state_code=state.id, address='address')
    session.add(buyer)
    session.commit()

    bill_1 = Bill(buyer_id=buyer.id, total_price=10, date=date.today(), purchase_order='order1', remarks='remarks1')
    bill_2 = Bill(buyer_id=buyer.id, total_price=100, date=date.today(), purchase_order='order2', remarks='remarks2')
    session.add(bill_1)
    session.add(bill_2)
    session.commit()

    # When: A request is sent to put a bill with updated data
    client.put('/api/v1/bills/2', json={'remarks': 'remarks3'})
    response = client.get('/api/v1/bills/2')

    # Then: The response should have a status code of 200 with updated bill
    assert response.status_code == 200
    assert response.json['remarks'] == 'remarks3'


def test_put_invalid_param(client):
    # Given: Bills in database
    # When: A request is sent to put a bill for invalid param
    response = client.put('/api/v1/bills/2', json={'buyer_id': 1})

    # Then: The response should have a status code of 422
    assert response.status_code == 422
    print(response.json)


def test_delete_bill(client, session):
    # Given: A bill in database
    state = IndianState(name='State', abbreviation='S')
    session.add(state)
    session.commit()

    buyer = Buyer(GST_No='123456789012345', name='buyer', state_code=state.id, address='address')
    session.add(buyer)
    session.commit()

    bill = Bill(buyer_id=buyer.id, total_price=10, date=date.today(), purchase_order='order1', remarks='remarks1')
    session.add(bill)
    session.commit()

    # When: A request is sent to delete a bill with id
    response = client.delete('/api/v1/bills/1')

    # Then: The response should have a status code of 204
    assert response.status_code == 204


def test_delete_non_existing_bill(client):
    # Given: A bill in database
    # When: A request is sent to delete a bill for not existing id
    response = client.delete('/api/v1/bills/1')

    # Then: The response should have a status code of 204
    assert response.status_code == 404
