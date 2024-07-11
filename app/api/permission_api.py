from flask.views import MethodView
from flask_smorest import Blueprint
from app.logger import logger
from app.models.permission import Permission
from app.schemas.permission_schema import PermissionSchema

permission_bp = Blueprint('permission_bp', __name__)


@permission_bp.route('/permission')
class PermissionListResponse(MethodView):
    @permission_bp.response(200, PermissionSchema(many=True))
    def get(self):
        logger.info("GET /permission called")
        permissions = Permission.query.order_by(Permission.name.asc()).all()
        return permissions
