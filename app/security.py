from flask_security import SQLAlchemyUserDatastore, Security

from app.models.user import User, Role
from app.extensions import db
from app.logger import logger


def init_security(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
    logger.info('Initialized security')
