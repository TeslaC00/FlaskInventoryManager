from flask.views import MethodView
from flask_security import hash_password
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from app.api.utils import apply_sorting
from app.models import User
from app.logger import logger
from app.extensions import db
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema, UserQuerySchema, UserResponseSchema
from app.datastore import user_datastore

user_bp = Blueprint('user_bp', __name__)


# TODO: add user form and schema
@user_bp.route('/user')
class UserListResource(MethodView):
    @user_bp.response(200, UserResponseSchema(many=True))
    @user_bp.arguments(UserQuerySchema, location='query')
    @user_bp.paginate()
    def get(self, query_args, pagination_parameters):
        logger.info('GET /user called')
        logger.debug(f"Query Arguments={query_args}")

        query = User.query
        # for filtering
        if 'email' in query_args:
            query = query.filter(User.email.like(f'%{query_args['email']}%'))
        if 'username' in query_args:
            query = query.filter(User.username.like(f'%{query_args['username']}%'))
        if 'active' in query_args:
            query = query.filter(User.active == query_args['active'])

        # for searching
        if 'search' in query_args:
            search = f"%{query_args['search']}%"
            query = query.filter(or_(
                User.name.like(search),
                User.email.like(search),
            ))
        # for sorting
        users = apply_sorting(query, query_args, pagination_parameters)
        logger.info(f"Found {pagination_parameters.item_count} users")
        logger.debug(f"Returned users: {users}")
        return users

    @user_bp.response(201, UserResponseSchema)
    @user_bp.arguments(UserCreateSchema)
    def post(self, new_user_data):
        logger.info('POST /user called')
        logger.debug(f"Creating new user with data: {new_user_data}")

        try:
            new_user = user_datastore.create_user(**new_user_data)
            new_user.password = hash_password(new_user_data['password'])
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"New user created with data id: {new_user.id}")
            return new_user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            abort(500, message="An error occurred while creating new user")


# decide whether to change the user id or not
@user_bp.route('/user/<int:user_id>')
class UserResource(MethodView):
    @user_bp.response(200, UserResponseSchema)
    def get(self, user_id):
        logger.info(f'GET /user/{user_id} called')
        user = User.query.get_or_404(user_id, description="Material not found")
        logger.info(f"Found user with id {user_id}")
        return user

    @user_bp.response(200, UserResponseSchema)
    @user_bp.arguments(UserUpdateSchema)
    def put(self, update_user_data, user_id):
        logger.info(f'PUT /user/{user_id} called')
        logger.debug(f"Updating user {user_id} with args: {update_user_data}")

        user = User.query.get_or_404(user_id, description="Material not found")
        for key, value in update_user_data.items():
            setattr(user, key, value)

        try:
            db.session.commit()
            logger.info(f"Updated user {user_id} with data: {update_user_data}")
            return user
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            abort(500, message="An error occurred while updating the user")

    @user_bp.response(204)
    def delete(self, user_id):
        logger.info(f'DELETE /user/{user_id} called')
        user = User.query.get_or_404(user_id, description="Material not found")
        try:
            db.session.delete(user)
            db.session.commit()
            logger.info(f"Deleted user {user_id}")
            return {'message': 'User deleted'}
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            abort(500, message="An error occurred while deleting the user")
