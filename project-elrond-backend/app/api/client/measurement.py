from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
import os
from dotenv import load_dotenv

from app.db.database import get_db 
from app.schemas.client_measurement import (
    ClientMeasurement, 
    ClientMeasurementCreate, 
    ClientMeasurementUpdate, 
    PaginatedMeasurementResponse
)
from app.crud.client_operations import measurements as crud_metrics 

router = APIRouter()

def get_current_client_id() -> UUID:
    # TODO auth
    return UUID(os.getenv("ID_CLIENT"))

@router.get(
    "/measurement",
    response_model=PaginatedMeasurementResponse[ClientMeasurement] 
)
def get_measurements(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):

    total_count = crud_metrics.count_measurements_by_client_id(
        db,
        client_id = get_current_client_id()
    )
    measurements = crud_metrics.read_measurements_by_client_id(
        db,
        client_id = get_current_client_id(),
        skip = skip,
          limit = limit
    )
    
    return {
        "total_count": total_count,
        "limit": limit,
        "skip": skip,
        "data": measurements
    }

@router.post(
    "/measurement",
    response_model=ClientMeasurement,
    status_code = status.HTTP_201_CREATED
)
def create_measurement(
    measurement_data: ClientMeasurementCreate,
    db: Session = Depends(get_db),
):

    db_measurement = crud_metrics.create_client_measurement(
        db, 
        measurement_data=measurement_data, 
        client_id = get_current_client_id()
    )
    return db_measurement

@router.get(
    "/measurement/{measurement_id}",
    response_model=ClientMeasurement
)
def get_measurement_by_id(
    measurement_id: UUID,
    db: Session = Depends(get_db)
):

    db_measurement = crud_metrics.read_measurement_by_id(db, measurement_id = measurement_id)

    if db_measurement is None or db_measurement.client_id != get_current_client_id():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found or access denied."
        )
    
    return db_measurement

@router.patch(
    "/measurement/{measurement_id}",
    response_model = ClientMeasurement
)
def update_measurement(
    measurement_update: ClientMeasurementUpdate,
    measurement_id: UUID,
    db: Session = Depends(get_db)
):
    
    db_measurement = crud_metrics.read_measurement_by_id(
        db,
        measurement_id
    )

    if db_measurement is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Measurement not found or access denied."
        )

    updated_measurement = crud_metrics.update_client_measurement(
        db, 
        measurement_id = measurement_id, 
        measurement_update = measurement_update
    )
    
    return updated_measurement

@router.delete(
    "/measurement/{measurement_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
def delete_measurement(
    measurement_id: UUID,
    db: Session = Depends(get_db)
):
    
    db_measurement = crud_metrics.read_measurement_by_id(
        db,
        measurement_id
    )

    if db_measurement is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Measurement not found or access denied."
        )

    crud_metrics.delete_client_measurement(
        db,
        measurement_id=measurement_id
    )
    
    return
