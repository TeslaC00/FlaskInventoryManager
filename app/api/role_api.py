from flask.views import MethodView
from flask_smorest import Blueprint, abort
from http import HTTPStatus

from app.errors.not_found_error import NotFoundError
from app.services.role_service import RoleService
from app.schemas.role_schema import RoleListResponseSchema, RoleQuerySchema, RoleCreateSchema, RoleUpdateSchema, \
    RoleResponseSchema
from app.logger import logger

role_bp = Blueprint('role_bp', __name__)


@role_bp.route('/role')
class RoleListResource(MethodView):
    @role_bp.response(HTTPStatus.OK, RoleListResponseSchema(many=True))
    @role_bp.arguments(RoleQuerySchema, location='query')
    def get(self, filters):
        logger.info('GET /role called')
        logger.debug(f"Query Arguments={filters}")

        try:
            roles = RoleService.get_all_roles(**filters)
            logger.debug(f"Returned roles: {roles}")
            return roles
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e, message=str(e))

    @role_bp.response(HTTPStatus.CREATED, RoleResponseSchema)
    @role_bp.arguments(RoleCreateSchema)
    def post(self, data):
        logger.info('POST /role called')
        logger.debug(f"Creating new role with data: {data}")
        # check if datastore generate duplicate role name errors
        try:
            role = RoleService.add_role(**data)
            logger.info(f"New Role created with ID {role.id}")
            return role
        except ValueError as ve:
            logger.error(f"Error creating role: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating role: {e}")
            abort(500, e)


@role_bp.route('/role/<int:role_id>')
class RoleResource(MethodView):
    @role_bp.response(HTTPStatus.OK, RoleResponseSchema)
    def get(self, role_id):
        logger.info(f'GET /role/{role_id} called')
        try:
            role = RoleService.get_role_by_id(role_id)
            logger.info(f"Found role with ID {role_id}")
            return role
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @role_bp.response(HTTPStatus.OK, RoleResponseSchema)
    @role_bp.arguments(RoleUpdateSchema)
    def put(self, data, role_id):
        logger.info(f'PUT /role/{role_id} called')
        logger.debug(f"Updating role {role_id} with args: {data}")

        try:
            role = RoleService.update_role(role_id, data)
            logger.info(f"Role {role_id} updated")
            return role
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error updating Role {role_id}: {e}")
            abort(500, e)

    @role_bp.response(HTTPStatus.NO_CONTENT)
    def delete(self, role_id):
        logger.info(f'DELETE /role/{role_id} called')
        try:
            RoleService.delete_role_by_id(role_id)
            logger.info(f"Role {role_id} deleted")
            return {'message': 'Role deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting role {role_id}: {e}")
            abort(500, e)
