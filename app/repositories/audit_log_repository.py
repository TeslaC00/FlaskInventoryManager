from typing import Optional

from sqlalchemy import or_

from app.extensions import db
from app.models import AuditLog
from app.errors.not_found_error import NotFoundError
from app.utils import apply_generic_sorting


class AuditLogRepository:
    @staticmethod
    def get_all(page: int = 1, per_page: int = 10, **filters: dict):
        query = AuditLog.query
        # for filtering
        if 'table_name' in filters:
            query = query.filter(AuditLog.table_name.like(f"%{filters['table_name']}%"))
        if 'table_primary_key' in filters:
            query = query.filter(AuditLog.table_primary_key.like(f"%{filters['table_primary_key']}%"))
        if 'column_name' in filters:
            query = query.filter(AuditLog.column_name.like(f"%{filters['column_name']}%"))
        if 'old_value' in filters:
            query = query.filter(AuditLog.old_value.like(f"%{filters['old_value']}%"))
        if 'new_value' in filters:
            query = query.filter(AuditLog.new_value.like(f"%{filters['new_value']}%"))
        if 'username' in filters:
            query = query.filter(AuditLog.username.like(f"%{filters['username']}%"))
        if 'start_timestamp' in filters:
            query = query.filter(AuditLog.change_timestamp >= filters['start_timestamp'])
        if 'end_timestamp' in filters:
            query = query.filter(AuditLog.change_timestamp <= filters['end_timestamp'])
        if 'action_type' in filters:
            query = query.filter(AuditLog.action_type.like(f"%{filters['action_type']}%"))
        # for searching
        if 'search' in filters:
            search = f"%{filters['search']}%"
            query = query.filter(or_(
                AuditLog.table_name.like(search),
                AuditLog.username.like(search),
                AuditLog.remarks.like(search)
            ))
        query = apply_generic_sorting(query, AuditLog, filters)
        return query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_by_id(audit_log_id: int) -> Optional[AuditLog]:
        return AuditLog.query.get(audit_log_id)

    @staticmethod
    def add(audit_log: AuditLog) -> AuditLog:
        db.session.add(audit_log)
        db.session.commit()
        return audit_log

    @staticmethod
    def update(audit_log: AuditLog) -> AuditLog:
        db.session.commit()
        return audit_log

    @staticmethod
    def delete(audit_log_id: int) -> None:
        audit_log = AuditLog.query.get(audit_log_id)
        if not audit_log:
            raise NotFoundError(f"AuditLog with id {audit_log_id} not found")

        db.session.delete(audit_log)
        db.session.commit()
