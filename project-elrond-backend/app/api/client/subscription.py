from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
import os
from dotenv import load_dotenv

from app.db.database import get_db
from app.schemas.client_subscription import (
    ClientSubscriptionCreate,
    ClientSubscriptionRead,
)
from app.crud.client_operations import subscription as crud_subs
from app.crud.trainer_operations.subscriptions import subscriptions as crud_tiers
from app.crud.trainer_operations.request import association as crud_assoc

router = APIRouter(tags=["Client Subscriptions"])

# TODO: Replace with proper JWT authentication
def get_current_client_id() -> UUID:
    load_dotenv()
    return UUID(os.getenv("ID_CLIENT"))

@router.get(
    "/subscriptions",
    response_model=List[ClientSubscriptionRead],
    description="Get all subscriptions for the current client.",
)
def get_all_client_subscriptions(db: Session = Depends(get_db)):
    client_id = get_current_client_id()
    return crud_subs.get_subscriptions_for_client(db, client_id=client_id)

@router.post(
    "/subscriptions/mock-buy",
    response_model=ClientSubscriptionRead,
    status_code=status.HTTP_201_CREATED,
    description="Mocked payment process (will be replaced with Stripe).",
)
def buy_subscription(
    purchase_data: ClientSubscriptionCreate, db: Session = Depends(get_db)
):
    client_id = get_current_client_id()
    trainer_id = purchase_data.trainer_id

    # 1. Security Check: Jsou vůbec propojení?
    if not crud_assoc.get_association_by_pair(db, client_id, trainer_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must have an association with this trainer before buying a subscription."
        )

    # 2. Business Logic Check: Existuje aktivní tier?
    db_tier = crud_tiers.get_tier_by_id_and_trainer(
        db, tier_id=purchase_data.tier_id, trainer_id=trainer_id
    )
    if not db_tier or not db_tier.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription tier not found or is currently inactive."
        )

    # 3. Conflict Check: Nemá už aktivní předplatné?
    if crud_subs.get_active_subscription(db, client_id, trainer_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have an active subscription for this trainer."
        )

    # 4. Action
    try:
        return crud_subs.create_mocked_subscription(
            db=db, client_id=client_id, data=purchase_data
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )