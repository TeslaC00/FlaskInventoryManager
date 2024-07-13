from app.errors.not_found_error import NotFoundError
from app.models import ProductionLog
from app.repositories.production_log_repository import ProductionLogRepository


class ProductionLogService:

    @staticmethod
    def get_all_production_logs(page: int = 1, per_page: int = 10, **filters: dict):
        try:
            return ProductionLogRepository.get_all(page=page, per_page=per_page, **filters)
        except Exception as e:
            raise RuntimeError(f"Error fetching ProductionLogs: {str(e)}")

    @staticmethod
    def get_production_log_by_id(production_log_id: int) -> ProductionLog:
        production_log = ProductionLogRepository.get_by_id(production_log_id)
        if not production_log:
            raise NotFoundError(f"ProductionLog with id {production_log_id} not found")
        return production_log

    @staticmethod
    def add_production_log(**data: dict) -> ProductionLog:
        production_log = ProductionLog(**data)
        try:
            log = ProductionLogRepository.add(production_log)
            from app.services.material_service import MaterialService
            from app.services.product_service import ProductService
            from app.services.product_material_service import ProductMaterialService

            ProductService.add_quantity(log.quantity_produced, log.product_part_no)
            for material in ProductService.get_product_by_id(log.product_part_no).materials:
                material_quantity = ProductMaterialService.get_product_material_by_id(log.product_part_no,
                                                                                      material.primary_key).quantity
                MaterialService.add_quantity(-material_quantity, material.primary_key)
            return log
        except ValueError as ve:
            raise ValueError(f"Invalid data: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Error creating ProductionLog: {str(e)}")

    @staticmethod
    def update_production_log(production_log_id: int, data: dict) -> ProductionLog:
        # Fetch existing production_log
        existing_production_log = ProductionLogService.get_production_log_by_id(production_log_id)

        # Update fields in the existing production_log
        for key, value in data.items():
            setattr(existing_production_log, key, value)

        # Pass updated production_log object to the repository
        try:
            return ProductionLogRepository.update(existing_production_log)
        except Exception as e:
            raise RuntimeError(f"Error updating ProductionLog: {str(e)}")

    @staticmethod
    def delete_production_log(production_log_id: int) -> None:
        try:
            log = ProductionLogService.get_production_log_by_id(production_log_id)
            from app.services.material_service import MaterialService
            from app.services.product_service import ProductService
            from app.services.product_material_service import ProductMaterialService

            ProductService.add_quantity(-log.quantity_produced, log.product_part_no)
            for material in ProductService.get_product_by_id(log.product_part_no).materials:
                material_quantity = ProductMaterialService.get_product_material_by_id(log.product_part_no,
                                                                                      material.primary_key).quantity
                MaterialService.add_quantity(material_quantity, material.primary_key)

            ProductionLogRepository.delete(production_log_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting ProductionLog: {str(e)}")
