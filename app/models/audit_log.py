# Audit_Log
# (
#   audit_id BIGINT NOT NULL AUTO_INCREMENT,
#   table_name VARCHAR(64) NOT NULL,
#   primary_key_value VARCHAR(255) NOT NULL,
#   column_name VARCHAR(64),
#   old_value LONGTEXT,
#   new_value LONGTEXT,
#   username VARCHAR(50) NOT NULL,
#   change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   action_type ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
#   PRIMARY KEY (audit_id)
# );
import enum
from datetime import datetime

from multipledispatch import dispatch
from sqlalchemy.sql import func

from app.database import db


class ActionType(enum.Enum):
    INSERT = 1
    UPDATE = 2
    DELETE = 3


class AuditLog(db.Model):
    """
    A model representing an audit log entry in the database.

    Attributes:
        id (int): The primary key and unique identifier for the audit log entry.
        table_name (str): The name of the table that the change occurred in.
        table_primary_key (str): The primary key value of the row that was changed.
        column_name (str): The name of the column that was changed.
        old_value (str): The value of the column before the change.
        new_value (str): The value of the column after the change.
        username (str): The username of the user who made the change. References the 'User.username' column.
        change_timestamp (datetime): The timestamp when the change was made.
        action_type (ActionType): The type of action performed (e.g., INSERT, UPDATE, DELETE).
        user (User): A relationship to the User model, back referenced by 'user'.

    Methods:
        to_dict(self):
            Converts the audit log entry into a dictionary.

        get_audit_logs():
            Overloaded method. Can be called with no parameters to retrieve all audit log entries, or with
            start_date and end_date parameters to retrieve entries within a specific timeframe.

            Without parameters:
                Retrieves all audit log entries, ordered by change_timestamp in descending order.

            With start_date, end_date (datetime, datetime):
                Retrieves audit log entries that occurred between start_date and end_date, inclusive,
                ordered by change_timestamp in descending order.

    Notes:
        - The username attribute is linked to the 'User.username' column, establishing a foreign key relationship.
        - The change_timestamp defaults to the current time when the log entry is created.
        - The action_type column uses the ActionType enum to ensure only valid actions are recorded.
    """
    __tablename__ = 'audit_log'
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    table_primary_key = db.Column(db.String(100), nullable=False)
    column_name = db.Column(db.String(100), nullable=False)
    old_value = db.Column(db.String(100), nullable=False)
    new_value = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), db.ForeignKey('user.username', name='fk_audit_log_user_username'),
                         nullable=False)
    change_timestamp = db.Column(db.DateTime, nullable=False, default=func.now())
    action_type = db.Column(db.Enum(ActionType), nullable=False)
    remarks = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'audit_id': self.id,
            'table_name': self.table_name,
            'table_primary_key': self.table_primary_key,
            'column_name': self.column_name,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'username': self.username,
            'change_timestamp': self.change_timestamp,
            'action_type': self.action_type,
            'remarks': self.remarks
        }

    @dispatch()
    def get_audit_logs(self):
        logs = AuditLog.query.order_by(AuditLog.change_timestamp.desc()).all()

        for log in logs:
            print(f"Time: {log.change_timestamp}, User: {log.username}, Action: {log.action_type}, "
                  f"Table: {log.table_name}, ID: {log.primary_key_value}, Column: {log.column_name}, "
                  f"Old Value: {log.old_value}, New Value: {log.new_value}")

    @dispatch(datetime, datetime)
    def get_audit_logs(self, start_date, end_date):
        # Ensure that start_date and end_date are datetime objects
        assert isinstance(start_date, datetime) and isinstance(end_date, datetime), "Dates must be datetime objects"

        # Filter records based on the change_timestamp column
        logs = AuditLog.query \
            .filter(AuditLog.change_timestamp >= start_date) \
            .filter(AuditLog.change_timestamp <= end_date) \
            .order_by(AuditLog.change_timestamp.desc()).all()

        for log in logs:
            print(f"Time: {log.change_timestamp}, User: {log.username}, Action: {log.action_type}, "
                  f"Table: {log.table_name}, ID: {log.primary_key_value}, Column: {log.column_name}, "
                  f"Old Value: {log.old_value}, New Value: {log.new_value}")
