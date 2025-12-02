from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
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
) -> Optional[ClientTrainerAssociation]:

    if get_association_by_pair(db, client_id, trainer_id):
        return None

    db_association = ClientTrainerAssociation(
        client_id=client_id,
        trainer_id=trainer_id,
        specialization_type=specialization_type,
    )

    try:
        db.add(db_association)
        db.flush()
        return db_association

    except IntegrityError:
        db.rollback()
        return None


def get_all_clients_for_trainer(
    db: Session, trainer_id: UUID
) -> List[ClientTrainerAssociation]:

    return (
        db.query(ClientTrainerAssociation)
        .filter(ClientTrainerAssociation.trainer_id == trainer_id)
        .all()
    )


def delete_association(db: Session, client_id: UUID, trainer_id: UUID) -> bool:

    db_association = get_association_by_pair(db, client_id, trainer_id)

    if db_association:
        db.delete(db_association)
        db.commit()
        return True
    return False
