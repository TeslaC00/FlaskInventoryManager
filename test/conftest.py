import os

import pytest
from dotenv import load_dotenv

from app import create_app
from app.extensions import db


@pytest.fixture(scope='session')
def app():
    os.environ['FLASK_ENV'] = 'testing'
    load_dotenv()
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()
