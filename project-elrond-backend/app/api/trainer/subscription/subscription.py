from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
import os
from dotenv import load_dotenv
from typing import List
from app.db.database import get_db 
from app.schemas.trainer_subscription_tier import (
    TrainerSubscriptionTier, 
    TrainerSubscriptionTierCreate, 
    TrainerSubscriptionTierUpdate,
)
from app.crud.trainer_operations.subscriptions import subscriptions as crud_tiers 

router = APIRouter()

# MOCK auth
def get_current_trainer_id() -> UUID:
    # TODO auth
    return UUID(os.getenv("ID_TRAINER"))


@router.get(
    "/tiers",
    response_model = List[TrainerSubscriptionTier]
)
def get_all_tiers_for_trainer(
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db),
):
    tiers = crud_tiers.read_tiers_by_trainer_id(
        db,
         trainer_id = trainer_id
    )
    
    if not tiers:
        return [] 
    
    return tiers


@router.get(
    "/tier/{tier_id}",
    response_model = TrainerSubscriptionTier
)
def get_tier_by_id(
    tier_id: UUID,
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db)
):
    db_tier = crud_tiers.read_tier_by_id(
        db,
        tier_id = tier_id
    )

    if db_tier is None or db_tier.trainer_id !=  trainer_id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Subscription Tier not found or access denied."
        )
    
    return db_tier


@router.post(
    "/tiers",
    response_model = TrainerSubscriptionTier,
    status_code = status.HTTP_201_CREATED
)
def create_tier(
    tier_data: TrainerSubscriptionTierCreate,
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db),
):
    
    db_tier = crud_tiers.create_subscription_tier(
        db, 
        tier_data = tier_data, 
        trainer_id = trainer_id
    )
    return db_tier


@router.patch(
    "/tier/{tier_id}",
    response_model = TrainerSubscriptionTier
)
def update_tier(
    tier_update: TrainerSubscriptionTierUpdate,
    tier_id: UUID,
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db),
):
    
    db_tier = crud_tiers.read_tier_by_id(
        db,
         tier_id
    )

    if db_tier is None or db_tier.trainer_id !=  trainer_id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Subscription Tier not found or access denied."
        )

    updated_tier = crud_tiers.update_subscription_tier(
        db, 
        tier_id = tier_id, 
        tier_update = tier_update
    )
    
    return updated_tier


@router.delete(
    "/tier/{tier_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
def delete_tier(
    tier_id: UUID,
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db),
):
    
    db_tier = crud_tiers.read_tier_by_id(
        db,
        tier_id
    )

    if db_tier is None or db_tier.trainer_id !=  trainer_id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Subscription Tier not found or access denied."
        )

    crud_tiers.delete_subscription_tier(
        db,
        tier_id = tier_id
    )
    
    return


@router.get(
    "/{trainer_id}/subscriptions",
    response_model=List[TrainerSubscriptionTier]
)
def get_tiers_for_public_view(
    trainer_id: UUID,
    db: Session = Depends(get_db),
):
    
    all_tiers = crud_tiers.read_tiers_by_trainer_id(
        db, 
        trainer_id=trainer_id
    )
    
    active_tiers = [tier for tier in all_tiers if tier.is_active]

    if not active_tiers:
        return [] 
    
    return active_tiers