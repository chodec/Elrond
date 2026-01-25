from sqlalchemy.orm import Session
from sqlalchemy import exc
from uuid import UUID
from typing import List, Optional

from app.db.models import TrainerSubscriptionTier
from app.schemas.trainer_subscription_tier import (
    TrainerSubscriptionTierCreate,
    TrainerSubscriptionTierUpdate,
)

def read_tier_by_id(db: Session, tier_id: UUID) -> Optional[TrainerSubscriptionTier]:
    return (
        db.query(TrainerSubscriptionTier)
        .filter(TrainerSubscriptionTier.id == tier_id)
        .first()
    )

def read_tiers_by_trainer_id(
    db: Session,
    trainer_id: UUID,
) -> List[TrainerSubscriptionTier]:
    return (
        db.query(TrainerSubscriptionTier)
        .filter(TrainerSubscriptionTier.trainer_id == trainer_id)
        .order_by(
            TrainerSubscriptionTier.is_active.desc(),
            TrainerSubscriptionTier.price_monthly.asc(),
        )
        .all()
    )

def create_subscription_tier(
    db: Session, tier_data: TrainerSubscriptionTierCreate, trainer_id: UUID
) -> TrainerSubscriptionTier:
    try:
        db_tier = TrainerSubscriptionTier(**tier_data.model_dump(), trainer_id=trainer_id)
        db.add(db_tier)
        db.commit()
        db.refresh(db_tier)
        return db_tier
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during tier creation: {str(e)}")

def update_subscription_tier(
    db: Session, tier_id: UUID, tier_update: TrainerSubscriptionTierUpdate
) -> TrainerSubscriptionTier:
    db_tier = read_tier_by_id(db, tier_id)

    if not db_tier:
        raise ValueError("Subscription tier not found")

    try:
        update_data = tier_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tier, key, value)

        db.commit()
        db.refresh(db_tier)
        return db_tier
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during tier update: {str(e)}")

def delete_subscription_tier(db: Session, tier_id: UUID) -> UUID:
    db_tier = read_tier_by_id(db, tier_id)

    if not db_tier:
        raise ValueError("Subscription tier not found")

    try:
        db.delete(db_tier)
        db.commit()
        return tier_id
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during tier deletion: {str(e)}")

def get_tier_by_id_and_trainer(
    db: Session, tier_id: UUID, trainer_id: UUID
) -> Optional[TrainerSubscriptionTier]:
    return (
        db.query(TrainerSubscriptionTier)
        .filter(
            TrainerSubscriptionTier.id == tier_id,
            TrainerSubscriptionTier.trainer_id == trainer_id,
        )
        .first()
    )