from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional, List
from uuid import UUID

from app.db.models import ClientTrainerAssociation

def get_association_by_pair(
    db: Session, client_id: UUID, trainer_id: UUID
) -> Optional[ClientTrainerAssociation]:
    return (
        db.query(ClientTrainerAssociation)
        .filter(
            ClientTrainerAssociation.client_id == client_id,
            ClientTrainerAssociation.trainer_id == trainer_id,
        )
        .first()
    )

def create_association(
    db: Session,
    client_id: UUID,
    trainer_id: UUID,
    specialization_type: Optional[str] = None,
) -> ClientTrainerAssociation:
    if get_association_by_pair(db, client_id, trainer_id):
        raise ValueError("Association already exists")

    try:
        db_association = ClientTrainerAssociation(
            client_id=client_id,
            trainer_id=trainer_id,
            specialization_type=specialization_type,
        )
        db.add(db_association)
        db.commit()
        db.refresh(db_association)
        return db_association
    except (IntegrityError, SQLAlchemyError) as e:
        db.rollback()
        raise RuntimeError(f"Database error during association creation: {str(e)}")

def get_all_clients_for_trainer(
    db: Session, trainer_id: UUID
) -> List[ClientTrainerAssociation]:
    return (
        db.query(ClientTrainerAssociation)
        .filter(ClientTrainerAssociation.trainer_id == trainer_id)
        .all()
    )

def delete_association(db: Session, client_id: UUID, trainer_id: UUID) -> UUID:
    db_association = get_association_by_pair(db, client_id, trainer_id)

    if not db_association:
        raise ValueError("Association not found")

    try:
        db.delete(db_association)
        db.commit()
        return client_id
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during association deletion: {str(e)}")