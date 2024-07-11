from flask.views import MethodView
from flask_smorest import Blueprint, abort
from http import HTTPStatus
from app.models.user import Role
from app.datastore import user_datastore
from app.schemas.role_schema import RoleListResponseSchema, RoleQuerySchema, RoleCreateSchema, RoleUpdateSchema, \
    RoleResponseSchema
from app.logger import logger
from app.extensions import db

role_bp = Blueprint('role_bp', __name__)


@role_bp.route('/role')
class RoleListResource(MethodView):
    @role_bp.response(HTTPStatus.OK, RoleListResponseSchema(many=True))
    @role_bp.arguments(RoleQuerySchema, location='query')
    def get(self, query_args):
        logger.info('GET /role called')
        logger.debug(f"Query Arguments={query_args}")

        query = Role.query

        # for searching
        if 'search' in query_args:
            query = query.filter(Role.name.like(f"%{query_args['search']}%"))

        # for sorting
        if 'sort_order' in query_args and query_args['sort_order'] == 'desc':
            query = query.order_by(Role.name.desc())
        else:
            query = query.order_by(Role.name.asc())

        count = query.count()
        roles = query.all()
        logger.info(f"Found {count} roles")
        logger.debug(f"Returned roles: {roles}")
        return roles

    @role_bp.response(HTTPStatus.CREATED, RoleResponseSchema)
    @role_bp.arguments(RoleCreateSchema)
    def post(self, new_role_data):
        logger.info('POST /role called')
        logger.debug(f"Creating new role with data: {new_role_data}")
        # check if datastore generate duplicate email or username errors
        try:
            new_role = user_datastore.create_role(**new_role_data)
            db.session.add(new_role)
            db.session.commit()
            logger.info(f"New role created with id: {new_role.id}")
            return new_role
        except Exception as e:
            logger.error(f"Error creating new role: {e}")
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="An error occurred while creating new role")


@role_bp.route('/role/<int:role_id>')
class RoleResource(MethodView):
    @role_bp.response(HTTPStatus.OK, RoleResponseSchema)
    def get(self, role_id):
        logger.info(f'GET /role/{role_id} called')
        role = Role.query.get_or_404(role_id, description='Role not found')
        logger.info(f"Found role with id {role_id}")
        return role

    @role_bp.response(HTTPStatus.OK, RoleResponseSchema)
    @role_bp.arguments(RoleUpdateSchema)
    def put(self, update_role_data, role_id):
        logger.info(f'PUT /role/{role_id} called')
        logger.debug(f"Updating user {role_id} with args: {update_role_data}")

        role = Role.query.get_or_404(role_id, description='Role not found')
        for key, value in update_role_data.items():
            setattr(role, key, value)

        try:
            db.session.commit()
            logger.info(f"Updated role {role_id} with data: {update_role_data}")
            return role
        except Exception as e:
            logger.error(f"Error updating role {role_id}: {e}")
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="An error occurred while updating the user")

    @role_bp.response(HTTPStatus.NO_CONTENT)
    def delete(self, role_id):
        logger.info(f'DELETE /role/{role_id} called')
        role = Role.query.get_or_404(role_id, description='Role not found')
        try:
            db.session.delete(role)
            db.session.commit()
            logger.info(f"Deleted role {role_id}")
            return {'message': 'Role deleted'}
        except Exception as e:
            logger.error(f"Error deleting role {role_id}: {e}")
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="An error occurred while deleting the role")
