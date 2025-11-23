from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
import os
from datetime import datetime

from app.db.database import get_db 
from app.schemas.client_subscription import ClientSubscriptionCreate, ClientSubscriptionRead
from app.crud.client_operations import subscription as crud_subs
from app.crud.trainer_operations.subscriptions import subscriptions as crud_tiers 
from app.crud.trainer_operations.request import association as crud_assoc 
from app.db.models import PaymentStatus, TrainerSubscriptionTier 

router = APIRouter()

# TODO:
def get_current_client_id() -> UUID:
    return UUID(os.getenv("ID_CLIENT")) 

@router.get(
    "/subscriptions",
    response_model=List[ClientSubscriptionRead],
    status_code=status.HTTP_200_OK,
    description="Get all active client subscription"
)
def get_all_client_subscriptions(
    db: Session = Depends(get_db)
):
    client_id = get_current_client_id()
    
    db_subscriptions = crud_subs.get_subscriptions_for_client(db, client_id=client_id)
    
    if not db_subscriptions:
        return [] 
        
    return db_subscriptions

@router.post(
    "/subscriptions/buy",
    response_model=ClientSubscriptionRead,
    status_code=status.HTTP_201_CREATED,
    description="Mock payment -> will be replaced with STRIPE"
)
def buy_subscription(
    purchase_data: ClientSubscriptionCreate,
    db: Session = Depends(get_db)
):
    
    client_id = get_current_client_id()
    trainer_id = purchase_data.trainer_id
    tier_id = purchase_data.tier_id
    
    if not crud_assoc.get_association_by_pair(db, client_id, trainer_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )

    db_tier: Optional[TrainerSubscriptionTier] = crud_tiers.get_tier_by_id_and_trainer(
        db, 
        tier_id=tier_id, 
        trainer_id=trainer_id
    )
    if not db_tier or not db_tier.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    if crud_subs.get_active_subscription(db, client_id, trainer_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT
        )

    db_subscription = crud_subs.create_mocked_subscription(
        db=db,
        client_id=client_id,
        data=purchase_data 
    )

    if db_subscription is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SvERVER_ERROR
        )
        
    # TODO: Trainer notification

    return db_subscription