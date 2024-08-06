from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.schemas.security_question_schema import SecurityQuestionListResponseSchema
from app.logger import logger
from app.services.security_question_service import SecurityQuestionService

security_question_bp = Blueprint('security_question_bp', __name__)


@security_question_bp.route('/security_question')
class SecurityQuestionListResource(MethodView):
    @security_question_bp.response(200, SecurityQuestionListResponseSchema(many=True))
    def get(self):
        logger.info('GET /role called')

        try:
            questions = SecurityQuestionService.get_all_questions()
            logger.debug(f"Returned security questions: {questions}")
            return questions
        except ValueError as ve:
            abort(400, ve)
        except Exception as e:
            abort(500, e, message=str(e))
