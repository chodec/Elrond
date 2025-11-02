from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from typing import Optional, List
from uuid import UUID
from app.db.models import ClientTrainerRequest, RequestStatus 

def get_request_by_id(db: Session, request_id: UUID) -> Optional[ClientTrainerRequest]:
    return db.query(ClientTrainerRequest).filter(ClientTrainerRequest.id == request_id).first()

def get_client_requests(db: Session, client_id: UUID) -> List[ClientTrainerRequest]:
    return db.query(ClientTrainerRequest).filter(ClientTrainerRequest.client_id == client_id).all()

def get_pending_requests_for_trainer(db: Session, trainer_id: UUID) -> List[ClientTrainerRequest]:
    return (
        db.query(ClientTrainerRequest)
        .filter(
            ClientTrainerRequest.trainer_id == trainer_id,
            ClientTrainerRequest.status == RequestStatus.PENDING
        )
        .all()
    )

def create_request(
    db: Session, 
    client_id: UUID, 
    trainer_id: UUID, 
    client_notes: Optional[str] = None
) -> Optional[ClientTrainerRequest]:

    db_request = ClientTrainerRequest(
        client_id=client_id,
        trainer_id=trainer_id,
        status=RequestStatus.PENDING,
        client_initial_notes=client_notes
    )
    
    try:
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        return db_request
    except IntegrityError:
        db.rollback()
        return None

def update_request_status(
    db: Session, 
    request: ClientTrainerRequest, 
    new_status: RequestStatus, 
    resolver_id: UUID, 
    resolution_notes: Optional[str] = None
) -> ClientTrainerRequest:

    if request.status == new_status:
        return request

    request.status = new_status
    request.resolved_by_user_id = resolver_id
    request.resolution_notes = resolution_notes
    
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def client_cancel_request(db: Session, request_id: UUID, client_id: UUID) -> Optional[ClientTrainerRequest]:
    request = get_request_by_id(db, request_id)
    if not request or request.client_id != client_id or request.status != RequestStatus.PENDING:
        return None 
        
    return update_request_status(
        db, 
        request, 
        RequestStatus.CANCELLED, 
        resolver_id=client_id, 
        resolution_notes="Cancelled by client"
    )

def trainer_resolve_request(
    db: Session, 
    request_id: UUID, 
    trainer_id: UUID, 
    new_status: RequestStatus, 
    notes: Optional[str] = None
) -> Optional[ClientTrainerRequest]:

    if new_status not in [RequestStatus.ACCEPTED, RequestStatus.REJECTED]:
        return None

    request = get_request_by_id(db, request_id)
    if not request or request.trainer_id != trainer_id or request.status != RequestStatus.PENDING:
        return None
        
    return update_request_status(
        db, 
        request, 
        new_status, 
        resolver_id=trainer_id, 
        resolution_notes=notes
    )