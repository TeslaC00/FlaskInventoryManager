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

from sqlalchemy.sql import func

from app.database import db


class ActionType(enum.Enum):
    INSERT = 1
    UPDATE = 2
    DELETE = 3


class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    audit_id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    table_primary_key = db.Column(db.String(100), nullable=False)
    column_name = db.Column(db.String(100), nullable=False)
    old_value = db.Column(db.String(100), nullable=False)
    new_value = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), db.ForeignKey('User.username'), nullable=False)
    change_timestamp = db.Column(db.DateTime, nullable=False, default=func.now())
    action_type = db.Column(db.Enum(ActionType), nullable=False)
    user = db.relationship('User', backref=db.backref('user'))

    def to_dict(self):
        return {
            'audit_id': self.audit_id,
            'table_name': self.table_name,
            'table_primary_key': self.table_primary_key,
            'column_name': self.column_name,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'username': self.username,
            'change_timestamp': self.change_timestamp,
            'action_type': self.action_type
        }
