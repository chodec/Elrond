from uuid import UUID
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class TrainerSubscriptionTierBase(BaseModel):

    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)

    price_monthly: Decimal = Field(..., gt=0, decimal_places=2)
    price_yearly: Optional[Decimal] = Field(None, gt=0, decimal_places=2)

    discount_percent: Decimal = Field(0, ge=0, le=100, decimal_places=2)

    is_active: bool = Field(True)

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}


class TrainerSubscriptionTierCreate(TrainerSubscriptionTierBase):
    pass


class TrainerSubscriptionTierUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)

    price_monthly: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    price_yearly: Optional[Decimal] = Field(None, gt=0, decimal_places=2)

    discount_percent: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)
    is_active: Optional[bool] = None

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}


class TrainerSubscriptionTier(TrainerSubscriptionTierBase):

    id: UUID
    trainer_id: UUID

    class Config:
        from_attributes = True
        json_encoders = {Decimal: lambda v: float(v)}
