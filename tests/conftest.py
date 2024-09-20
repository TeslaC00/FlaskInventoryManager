import pytest

from app import create_app
from app.extensions import db
from app.models import Unit, Product


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session

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

# test if price value calculated is right
# test kro fail ho rha hai bina attributes ke
# test kro fail ho rha hai galat attribute values pe