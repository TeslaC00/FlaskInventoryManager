from typing import Optional

from app.extensions import db
from app.models import Unit
from app.errors.not_found_error import NotFoundError


class UnitRepository:
    @staticmethod
    def get_all():
        return Unit.query.all()

    @staticmethod
    def get_by_id(unit_id: int) -> Optional[Unit]:
        return Unit.query.get(unit_id)

    @staticmethod
    def add(unit: Unit) -> Unit:
        db.session.add(unit)
        db.session.commit()
        return unit

    @staticmethod
    def update(unit: Unit) -> Unit:
        db.session.commit()
        return unit

    @staticmethod
    def delete(unit_id: int) -> None:
        unit = Unit.query.get(unit_id)
        if not unit:
            raise NotFoundError(f"Unit with id {unit_id} not found")

        db.session.delete(unit)
        db.session.commit()
