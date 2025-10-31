from uuid import UUID
from typing import Optional, TypeVar, List, Generic
import datetime
from decimal import Decimal 
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class PaginatedMeasurementResponse(GenericModel, Generic[T]):
    total_count: int = Field(...)
    limit: int = Field(...)
    skip: int = Field(...)
    data: List[T]

class ClientMeasurementBase(BaseModel):
    date: datetime.datetime = Field(...)
    
    body_weight: Decimal = Field(..., gt = 0)
    biceps_size: Optional[Decimal] = Field(None, gt = 0)
    waist_size: Optional[Decimal] = Field(None, gt = 0)
    chest_size: Optional[Decimal] = Field(None, gt = 0)
    thigh_size: Optional[Decimal] = Field(None, gt = 0)
    
    notes: Optional[str] = Field(None, max_length = 500)

class ClientMeasurementCreate(ClientMeasurementBase):
   pass 

class ClientMeasurement(ClientMeasurementBase):
    id: UUID
    
    class Config:
        from_attributes = True
        
class ClientMeasurementUpdate(BaseModel):
    date: Optional[datetime.datetime] = None
    
    body_weight: Optional[Decimal] = Field(None, gt = 0)
    biceps_size: Optional[Decimal] = Field(None, gt = 0)
    waist_size: Optional[Decimal] = Field(None, gt = 0)
    chest_size: Optional[Decimal] = Field(None, gt = 0)
    thigh_size: Optional[Decimal] = Field(None, gt = 0)
    
    notes: Optional[str] = Field(None, max_length = 500)