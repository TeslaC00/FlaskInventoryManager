from datetime import datetime
from werkzeug.routing import BaseConverter, ValidationError


class DateConverter(BaseConverter):
    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError(f"Invalid date format: {value}. Use YYYY-MM-DD.")

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')
