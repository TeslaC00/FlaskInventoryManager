import enum
from datetime import datetime

from multipledispatch import dispatch
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from sqlalchemy.sql import func
from app.extensions import db


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
    id = Column(Integer, primary_key=True)
    table_name = Column(String(100), nullable=False)
    table_primary_key = Column(String(100), nullable=False)
    column_name = Column(String(100), nullable=False)
    old_value = Column(String(100), nullable=False)
    new_value = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    change_timestamp = Column(DateTime, nullable=False, default=func.now())
    action_type = Column(Enum(ActionType), nullable=False)
    remarks = Column(Text, nullable=True)

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
