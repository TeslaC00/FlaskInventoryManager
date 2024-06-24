import os

import pytest
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

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
def test_client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope='module')
def init_database(test_app):
    db = SQLAlchemy(test_app)
    db.create_all()
    yield db

    db.drop_all()


@pytest.fixture(scope='function')
def session(init_database):
    db = init_database
    db.session.begin_nested()
    yield db.session
    db.session.rollback()
    db.session.close()
