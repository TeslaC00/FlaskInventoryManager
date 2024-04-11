# test_app.py
from app.database import db


def test_base(client):
    response = client.get('/')
    assert response.status_code == 200


# Tests the database connection
def test_database_connection(client):
    from app.models import User

    # Create a test user record
    test_user = User(username='test_user', password='password', role='user')
    db.session.add(test_user)
    db.session.commit()

    # Query the test user from the database
    queried_user = User.query.filter_by(username='test_user').first()

    # Assert that the queried user exists
    assert queried_user is not None
