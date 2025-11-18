from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exc
from uuid import UUID
from datetime import datetime, timedelta
from typing import Optional, List
from decimal import Decimal

from app.db.models import ClientSubscription, TrainerSubscriptionTier, ClientTrainerAssociation, PaymentStatus
from app.schemas.client_subscription import ClientSubscriptionCreate 
from app.crud.trainer_operations.subscriptions import subscriptions as crud_tiers 

def _calculate_end_date(tier: TrainerSubscriptionTier) -> datetime:

    today = datetime.now()
    
    if tier.price_yearly is not None and tier.price_yearly > 0:
        return today + timedelta(days=365)
    else:
        return today + timedelta(days=30)

def get_active_subscription(
    db: Session, 
    client_id: UUID, 
    trainer_id: UUID
) -> Optional[ClientSubscription]:
    
    return db.query(ClientSubscription).options(
        joinedload(ClientSubscription.tier)
    ).filter(
        ClientSubscription.client_id == client_id,
        ClientSubscription.trainer_id == trainer_id,
        ClientSubscription.status == PaymentStatus.MOCKED_PAID,
        ClientSubscription.end_date > datetime.now() 
    ).first()

def get_subscriptions_for_client(
    db: Session, 
    client_id: UUID
) -> List[ClientSubscription]:
    return db.query(ClientSubscription).options(
        joinedload(ClientSubscription.tier)
    ).filter(
        ClientSubscription.client_id == client_id
    ).order_by(ClientSubscription.start_date.desc()).all()


def create_mocked_subscription(
    db: Session, 
    client_id: UUID, 
    data: ClientSubscriptionCreate 
) -> Optional[ClientSubscription]:


    tier = crud_tiers.get_tier_by_id_and_trainer(
        db, 
        tier_id=data.tier_id, 
        trainer_id=data.trainer_id
    )
    if not tier:
        return None

    end_date = _calculate_end_date(tier)

    db_subscription = ClientSubscription(
        client_id=client_id,
        trainer_id=data.trainer_id,
        tier_id=data.tier_id,
        end_date=end_date,
        status=PaymentStatus.MOCKED_PAID
    )

    try:
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription
        
    except exc.IntegrityError:
        db.rollback()
        return None
    except Exception:
        db.rollback()
        return None