from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import os
from typing import List
from app.db.database import get_db
from app.schemas.client_trainer_request import RequestRead, TrainerResolution
from app.crud.trainer_operations.request.client_trainer_requests import (
    get_pending_requests_for_trainer,
    trainer_resolve_request,
)
from app.db.models import RequestStatus

router = APIRouter(tags=["Trainer Requests"])

# TODO: Nahradit skutečným JWT dekódováním
def get_current_trainer_id() -> UUID:
    return UUID(os.getenv("ID_TRAINER"))

@router.get(
    "/requests/pending",
    response_model=List[RequestRead],
    description="Get all pending client requests for the current trainer.",
)
def get_all_pending_requests(db: Session = Depends(get_db)):
    trainer_id = get_current_trainer_id()
    # Pokud nejsou žádné žádosti, vracíme prázdný list (200 OK []), ne 404.
    return get_pending_requests_for_trainer(db=db, trainer_id=trainer_id)

@router.patch(
    "/request/{request_id}/approve",
    response_model=RequestRead,
    description="Approve a client request. This creates a formal association.",
)
def approve_client_request(
    request_id: UUID, 
    resolution_data: TrainerResolution, 
    db: Session = Depends(get_db)
):
    trainer_id = get_current_trainer_id()
    
    try:
        return trainer_resolve_request(
            db=db,
            request_id=request_id,
            trainer_id=trainer_id,
            new_status=RequestStatus.ACCEPTED,
            notes=resolution_data.resolution_notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        # Sem spadne i chyba, pokud by selhalo vytvoření asociace
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch(
    "/request/{request_id}/reject",
    response_model=RequestRead,
    description="Reject a client request.",
)
def reject_client_request(
    request_id: UUID, 
    resolution_data: TrainerResolution, 
    db: Session = Depends(get_db)
):
    trainer_id = get_current_trainer_id()
    
    try:
        return trainer_resolve_request(
            db=db,
            request_id=request_id,
            trainer_id=trainer_id,
            new_status=RequestStatus.REJECTED,
            notes=resolution_data.resolution_notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))