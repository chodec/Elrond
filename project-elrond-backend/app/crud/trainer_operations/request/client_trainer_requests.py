from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional, List
from uuid import UUID
from app.db.models import ClientTrainerRequest, RequestStatus
from app.crud.trainer_operations.request.association import create_association

def get_request_by_id(db: Session, request_id: UUID) -> Optional[ClientTrainerRequest]:
    return (
        db.query(ClientTrainerRequest)
        .filter(ClientTrainerRequest.id == request_id)
        .first()
    )

def get_client_requests(db: Session, client_id: UUID) -> List[ClientTrainerRequest]:
    return (
        db.query(ClientTrainerRequest)
        .filter(ClientTrainerRequest.client_id == client_id)
        .all()
    )

def get_pending_requests_for_trainer(
    db: Session, trainer_id: UUID
) -> List[ClientTrainerRequest]:
    return (
        db.query(ClientTrainerRequest)
        .filter(
            ClientTrainerRequest.trainer_id == trainer_id,
            ClientTrainerRequest.status == RequestStatus.PENDING,
        )
        .all()
    )

def create_request(
    db: Session, client_id: UUID, trainer_id: UUID, client_notes: Optional[str] = None
) -> ClientTrainerRequest:
    existing_pending_request = (
        db.query(ClientTrainerRequest)
        .filter(
            ClientTrainerRequest.client_id == client_id,
            ClientTrainerRequest.trainer_id == trainer_id,
            ClientTrainerRequest.status == RequestStatus.PENDING,
        )
        .first()
    )

    if existing_pending_request:
        raise ValueError("A pending request already exists between this client and trainer")

    try:
        db_request = ClientTrainerRequest(
            client_id=client_id,
            trainer_id=trainer_id,
            status=RequestStatus.PENDING,
            client_initial_notes=client_notes,
        )
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        return db_request
    except (IntegrityError, SQLAlchemyError) as e:
        db.rollback()
        raise RuntimeError(f"Database error during request creation: {str(e)}")

def update_request_status(
    db: Session,
    request: ClientTrainerRequest,
    new_status: RequestStatus,
    resolver_id: UUID,
    resolution_notes: Optional[str] = None,
) -> ClientTrainerRequest:
    try:
        if request.status != new_status:
            request.status = new_status
            request.resolved_by_user_id = resolver_id
            request.resolution_notes = resolution_notes
            
            db.add(request)
            db.commit()
            db.refresh(request)
        return request
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during status update: {str(e)}")

def client_cancel_request(
    db: Session, request_id: UUID, client_id: UUID
) -> ClientTrainerRequest:
    request = get_request_by_id(db, request_id)
    if not request or request.client_id != client_id:
        raise ValueError("Request not found or not owned by client")
    
    if request.status != RequestStatus.PENDING:
        raise ValueError("Only pending requests can be cancelled")

    return update_request_status(
        db,
        request,
        RequestStatus.CANCELLED,
        resolver_id=client_id,
        resolution_notes="Cancelled by client",
    )

def trainer_resolve_request(
    db: Session,
    request_id: UUID,
    trainer_id: UUID,
    new_status: RequestStatus,
    notes: Optional[str] = None,
) -> ClientTrainerRequest:
    if new_status not in [RequestStatus.ACCEPTED, RequestStatus.REJECTED]:
        raise ValueError("Invalid target status for trainer resolution")

    request = get_request_by_id(db, request_id)
    if not request or request.trainer_id != trainer_id:
        raise ValueError("Request not found for this trainer")
    
    if request.status != RequestStatus.PENDING:
        raise ValueError("Request is already resolved")

    if new_status == RequestStatus.ACCEPTED:
        try:
            create_association(db, request.client_id, trainer_id)
        except (ValueError, RuntimeError) as e:
            raise RuntimeError(f"Could not accept request: {str(e)}")

    return update_request_status(
        db, request, new_status, resolver_id=trainer_id, resolution_notes=notes
    )