from flask import current_app
from app.logger import logger


def create_users():
    if current_app.testing:
        logger.debug("In Testing skipping create users")
        return
    with current_app.app_context():
        current_app.security.datastore.find_or_create_role(
            name='user',
            description="Administrator role",
            permissions={'user-read', 'user-write'}
        )
        current_app.security.datastore.find_or_create_role(
            name='admin',
            description="User role",
            permissions={'admin-read', 'admin-write'}
        )
        if not current_app.security.datastore.find_user(email='user@gmail.com'):
            current_app.security.datastore.create_user(
                email='user@gmail.com', username='user', password='pass',
                security_question=1,
                security_answer="Yes",
                roles=['user'],
            )
        if not current_app.security.datastore.find_user(email='admin@gmail.com'):
            current_app.security.datastore.create_user(
                email='admin@gmail.com', username='admin', password='admin',
                security_question=2,
                security_answer="Yes",
                roles=['admin', 'user'],
            )
        current_app.security.datastore.db.session.commit()
        logger.debug('Created Default Users')
