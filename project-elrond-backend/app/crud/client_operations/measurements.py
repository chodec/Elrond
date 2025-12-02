from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from app.db.models import ClientMeasurement
from app.schemas.client_measurement import (
    ClientMeasurementCreate,
    ClientMeasurementUpdate,
)


def read_measurement_by_id(
    db: Session, measurement_id: UUID
) -> Optional[ClientMeasurement]:
    return (
        db.query(ClientMeasurement)
        .filter(ClientMeasurement.id == measurement_id)
        .first()
    )


def count_measurements_by_client_id(db: Session, client_id: UUID) -> int:
    return (
        db.query(ClientMeasurement)
        .filter(ClientMeasurement.client_id == client_id)
        .count()
    )  # get rows returned


def read_measurements_by_client_id(
    db: Session, client_id: UUID, skip: int = 0, limit: int = 10  # paging
) -> List[ClientMeasurement]:

    return (
        db.query(ClientMeasurement)
        .filter(ClientMeasurement.client_id == client_id)
        .order_by(ClientMeasurement.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_client_measurement(
    db: Session, measurement_data: ClientMeasurementCreate, client_id: UUID
) -> ClientMeasurement:
    db_measurement = ClientMeasurement(
        **measurement_data.model_dump(), client_id=client_id
    )
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement


def update_client_measurement(
    db: Session, measurement_id: UUID, measurement_update: ClientMeasurementUpdate
) -> Optional[ClientMeasurement]:
    db_measurement = read_measurement_by_id(db, measurement_id)

    if db_measurement:
        update_data = measurement_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_measurement, key, value)

        db.commit()
        db.refresh(db_measurement)
        return db_measurement
    return None


def delete_client_measurement(db: Session, measurement_id: UUID) -> Optional[UUID]:
    db_measurement = read_measurement_by_id(db, measurement_id)

    if db_measurement:
        db.delete(db_measurement)
        db.commit()
        return measurement_id
    return None
