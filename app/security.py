from flask_security import SQLAlchemyUserDatastore, Security

from app.models.user import User, Role
from app.extensions import db
from app.logger import logger


def init_security(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
    logger.info('Initialized security')
    with app.app_context():
        if not user_datastore.find_role('user'):
            user_datastore.create_role(name='user', permissions={'user-read', 'user-write'})
        if not user_datastore.find_role('admin'):
            user_datastore.create_role(name='admin', permissions={'admin-read', 'admin-write'})
        if not user_datastore.find_user(email='user@gmail.com'):
            user_datastore.create_user(email='user@gmail.com', password='user', roles=['user'])
        db.session.commit()
