from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import os
from dotenv import load_dotenv
from typing import List
from app.db.database import get_db 
from app.schemas.client_trainer_request import RequestCreate, RequestRead
from app.crud.trainer_operations.request.client_trainer_requests import create_request, client_cancel_request, get_client_requests
from app.db.models import RequestStatus 

def get_current_client_id() -> UUID:
    # TODO auth
    return UUID(os.getenv("ID_CLIENT")) 

router = APIRouter()

@router.post(
    "/request", 
    response_model=RequestRead, 
    status_code=status.HTTP_201_CREATED
)
def submit_new_trainer_request(
    request_data: RequestCreate,
    db: Session = Depends(get_db) 
):

    client_id = get_current_client_id()
    
    try:
        db_request = create_request(
            db=db,
            client_id=client_id,
            trainer_id=request_data.trainer_id,
            client_notes=request_data.client_initial_notes
        )
        
        if db_request is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Request exists"
            )
        
        return db_request
    
    except Exception as e:
       print(e)
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Internal server error"
        )

@router.patch(
    "/request/{request_id}/cancel",
    response_model=RequestRead
)
def cancel_own_trainer_request(
    request_id: UUID,
    db: Session = Depends(get_db)
):

    client_id = get_current_client_id()
    
    db_request = client_cancel_request(
        db=db,
        request_id=request_id,
        client_id=client_id
    )
    
    if db_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return db_request
    
@router.get(
    "/requests/",
    response_model=List[RequestRead]
)
def get_all_client_requests(
    db: Session = Depends(get_db)
):
    client_id = get_current_client_id()
    db_requests = get_client_requests(db=db, client_id=client_id)
    
    if not db_requests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    return db_requests