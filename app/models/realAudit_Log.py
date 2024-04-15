from app.database import db
from sqlalchemy.dialects.mysql import BIGINT, LONGTEXT, ENUM

class Audit_Log(db.Model):
    """
    Represents an audit log record in the database.
    This model stores the history of changes made to various database tables, useful for audit trails.

    Attributes:
        __tablename__ (str): Name of this audit table in the database.
        audit_id (BIGINT): Unique identifier for each audit log entry. Auto-increments.
        table_name (str): Name of the table where the change occurred.
        primary_key_value (str): The primary key value of the row that was changed.
        column_name (str): Name of the column that was changed.
        old_value (LONGTEXT): The old value of the column before the change.
        new_value (LONGTEXT): The new value of the column after the change.
        username (str): The username of the individual who made the change.
        change_timestamp (TIMESTAMP): The timestamp when the change was made.
        action_type (ENUM): The type of action performed ('INSERT', 'UPDATE', 'DELETE').
    """
    __tablename__ = 'audit_log'
    audit_id = db.Column(BIGINT, primary_key=True, autoincrement=True)
    table_name = db.Column(db.String(64), nullable=False)
    primary_key_value = db.Column(db.String(255), nullable=False)
    column_name = db.Column(db.String(64), nullable=True)
    old_value = db.Column(LONGTEXT, nullable=True)
    new_value = db.Column(LONGTEXT, nullable=True)
    username = db.Column(db.String(50), nullable=False)
    change_timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    action_type = db.Column(ENUM('INSERT', 'UPDATE', 'DELETE'), nullable=False)

    def to_dict(self):
        return {
            'audit_id': self.audit_id,
            'table_name': self.table_name,
            'primary_key_value': self.primary_key_value,
            'column_name': self.column_name,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'username': self.username,
            'change_timestamp': self.change_timestamp,
            'action_type': self.action_type
        }
