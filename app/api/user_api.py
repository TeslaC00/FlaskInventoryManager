from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema, UserQuerySchema, UserResponseSchema, \
    UserListResponseSchema
from app.services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user')
class UserListResource(MethodView):
    @user_bp.response(200, UserListResponseSchema(many=True))
    @user_bp.arguments(UserQuerySchema, location='query')
    @user_bp.paginate()
    def get(self, filters, pagination_parameters):
        logger.info('GET /user called')
        logger.debug(f"Query Arguments={filters}")

        try:
            users = UserService.get_all_users(pagination_parameters.page, pagination_parameters.page_size,
                                              **filters) 
            for user in users.items:
                user.password = "REDACTED"
            pagination_parameters.item_count = users.total
            logger.info(f"Found {pagination_parameters.item_count} users")
            logger.debug(f"Returned users: {users}")
            return users
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e, message=str(e))

    @user_bp.response(201, UserResponseSchema)
    @user_bp.arguments(UserCreateSchema)
    def post(self, data):
        logger.info('POST /user called')
        logger.debug(f"Creating new user with data: {data}")
        # check if datastore generate duplicate email or username errors
        try:
            user = UserService.add_user(**data)
            logger.info(f"New User created with ID {user.id}")
            return user
        except ValueError as ve:
            logger.error(f"Error creating user: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            abort(500, e)


# decide whether to change the user id or not in log info
@user_bp.route('/user/<int:user_id>')
class UserResource(MethodView):
    @user_bp.response(200, UserResponseSchema)
    def get(self, user_id):
        logger.info(f'GET /user/{user_id} called')
        try:
            user = UserService.get_user_by_id(user_id)
            logger.info(f"Found user with ID {user_id}")
            return user
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @user_bp.response(200, UserResponseSchema)
    @user_bp.arguments(UserUpdateSchema)
    def put(self, data, user_id):
        logger.info(f'PUT /user/{user_id} called')
        logger.debug(f"Updating user {user_id} with args: {data}")

        try:
            user = UserService.update_user(user_id, data)
            logger.info(f"User {user_id} updated")
            return user
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating User {user_id}: {e}")
            abort(500, e)

    @user_bp.response(204)
    def delete(self, user_id):
        logger.info(f'DELETE /user/{user_id} called')
        try:
            UserService.delete_user_by_id(user_id)
            logger.info(f"User {user_id} deleted")
            return {'message': 'User deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            abort(500, e)
