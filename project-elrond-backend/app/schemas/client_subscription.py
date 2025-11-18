from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal
from app.db.models import PaymentStatus

class ClientSubscriptionTierInfo(BaseModel):
    id: UUID
    name: str
    price_monthly: Decimal
    price_yearly: Optional[Decimal]
    discount_percent: Decimal
    
    class Config:
        from_attributes = True


class ClientSubscriptionCreate(BaseModel):
    
    tier_id: UUID = Field(...)
    trainer_id: UUID = Field(...)


class ClientSubscriptionRead(BaseModel):
    id: UUID
    client_id: UUID
    trainer_id: UUID
    
    start_date: datetime
    end_date: datetime
    status: PaymentStatus
    
    tier: ClientSubscriptionTierInfo 
    
    class Config:
        from_attributes = True