from app.errors.not_found_error import NotFoundError
from app.models import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:
    @staticmethod
    def get_all_audit_logs(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return AuditLogRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching AuditLog: {str(e)}")

    @staticmethod
    def get_audit_log_by_id(audit_log_id: int) -> AuditLog:
        audit_log = AuditLogRepository.get_by_id(audit_log_id)
        if not audit_log:
            raise NotFoundError(f"AuditLog with id {audit_log_id} not found")
        return audit_log

    @staticmethod
    def add_audit_log(**data: dict) -> AuditLog:
        audit_log = AuditLog(**data)
        try:
            return AuditLogRepository.add(audit_log)
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating AuditLog: {str(e)}")

    @staticmethod
    def update_audit_log(audit_log_id: int, data: dict) -> AuditLog:
        # Fetch existing audit_log
        existing_audit_log = AuditLogService.get_audit_log_by_id(audit_log_id)

        # Update fields in the existing audit_log
        for key, value in data.items():
            setattr(existing_audit_log, key, value)

        # Pass updated audit_log object to the repository
        try:
            return AuditLogRepository.update(existing_audit_log)
        except Exception as e:
            raise RuntimeError(f"Error updating AuditLog: {str(e)}")

    @staticmethod
    def delete_audit_log(audit_log_id: int) -> None:
        try:
            AuditLogRepository.delete(audit_log_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting AuditLog: {str(e)}")
