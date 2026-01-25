from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import os
from dotenv import load_dotenv
from typing import List
from app.db.database import get_db
from app.schemas.client_trainer_request import RequestCreate, RequestRead
from app.crud.trainer_operations.request.client_trainer_requests import (
    create_request,
    client_cancel_request,
    get_client_requests,
)

# TODO: Replace with proper JWT authentication
def get_current_client_id() -> UUID:
    load_dotenv()
    return UUID(os.getenv("ID_CLIENT"))

router = APIRouter(tags=["Client Requests"])

@router.post(
    "/request",
    response_model=RequestRead,
    status_code=status.HTTP_201_CREATED,
    description="Initiate relationship with trainer.",
)
def submit_new_trainer_request(
    request_data: RequestCreate, db: Session = Depends(get_db)
):
    client_id = get_current_client_id()

    try:
        return create_request(
            db=db,
            client_id=client_id,
            trainer_id=request_data.trainer_id,
            client_notes=request_data.client_initial_notes,
        )
    except ValueError as e:
        # Převedeme logickou chybu (již existující pending request) na 409 Conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch(
    "/request/{request_id}/cancel",
    response_model=RequestRead,
    description="Cancel initiated relationship with trainer.",
)
def cancel_own_trainer_request(request_id: UUID, db: Session = Depends(get_db)):
    client_id = get_current_client_id()

    try:
        return client_cancel_request(
            db=db, request_id=request_id, client_id=client_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/requests/",
    response_model=List[RequestRead],
    description="Get all requests sent to trainers by the current client.",
)
def get_all_client_requests(db: Session = Depends(get_db)):
    client_id = get_current_client_id()
    # Listy vracíme i prázdné (200 OK []), 404 pro seznamy není standardní
    return get_client_requests(db=db, client_id=client_id)