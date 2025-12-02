from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
import os
from typing import List
from app.db.database import get_db
from app.schemas.client_trainer_request import RequestRead, TrainerResolution
from app.crud.trainer_operations.request.client_trainer_requests import (
    get_pending_requests_for_trainer,
    trainer_resolve_request,
)
from app.db.models import RequestStatus

router = APIRouter()


def get_current_trainer_id() -> UUID:
    # TODO auth
    return UUID(os.getenv("ID_TRAINER"))


@router.get(
    "/requests/pending",
    response_model=List[RequestRead],
    description="Check any pending requests from clients",
)
def get_all_pending_requests(db: Session = Depends(get_db)):
    trainer_id = get_current_trainer_id()
    db_requests = get_pending_requests_for_trainer(db=db, trainer_id=trainer_id)

    if not db_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_requests


@router.patch(
    "/request/{request_id}/approve",
    response_model=RequestRead,
    description="Approve request from the cliend -> he will be asked for money",
)
def approve_client_request(
    request_id: UUID, resolution_data: TrainerResolution, db: Session = Depends(get_db)
):

    trainer_id = get_current_trainer_id()
    db_request = trainer_resolve_request(
        db=db,
        request_id=request_id,
        trainer_id=trainer_id,
        new_status=RequestStatus.ACCEPTED,
        notes=resolution_data.resolution_notes,
    )

    if db_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_request


@router.patch(
    "/request/{request_id}/reject",
    response_model=RequestRead,
    description="Reject client relationship request -> you might not want another clients",
)
def reject_client_request(
    request_id: UUID, resolution_data: TrainerResolution, db: Session = Depends(get_db)
):

    trainer_id = get_current_trainer_id()
    db_request = trainer_resolve_request(
        db=db,
        request_id=request_id,
        trainer_id=trainer_id,
        new_status=RequestStatus.REJECTED,
        notes=resolution_data.resolution_notes,
    )

    if db_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_request
