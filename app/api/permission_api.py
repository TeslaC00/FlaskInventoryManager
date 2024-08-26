from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.errors.not_found_error import NotFoundError
from app.logger import logger
from app.services.permission_service import PermissionService
from app.schemas.permission_schema import PermissionSchema, PermissionResponseSchema

permission_bp = Blueprint('permission_bp', __name__)


@permission_bp.route('/permission')
class PermissionListResponse(MethodView):
    @permission_bp.response(200, PermissionResponseSchema(many=True))
    def get(self):
        logger.info("GET /permission called")
        try:
            return PermissionService.get_all_permissions()
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e)

    @permission_bp.response(200, PermissionResponseSchema)
    @permission_bp.arguments(PermissionSchema)
    def post(self, data):
        logger.info("POST /permission called")
        try:
            return PermissionService.add_permission(**data)
        except ValueError as ve:
            logger.error(f"Error creating Material: {ve}")
            abort(400, ve)
        except Exception as e:
            logger.error(f"Error creating Material: {e}")
            abort(500, e)


@permission_bp.route('/permission/<int:permission_id>')
class PermissionResponse(MethodView):
    @permission_bp.response(200, PermissionResponseSchema)
    def get(self, permission_id):
        logger.info("GET /permission called")
        try:
            permission = PermissionService.get_permission_by_id(permission_id)
            logger.info(f"Found material with part_no {permission_id}")
            return permission
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            abort(500, e)

    @permission_bp.response(204)
    def delete(self, permission_id):
        logger.info(f"DELETE /permission/{permission_id} called")
        try:
            PermissionService.delete_permission(permission_id)
            logger.info(f"Permission {permission_id} deleted")
            return {'message': 'Permission deleted'}
        except NotFoundError as nfe:
            abort(404, nfe)
        except Exception as e:
            logger.error(f"Error deleting Permission {permission_id}: {e}")
            abort(500, e)
