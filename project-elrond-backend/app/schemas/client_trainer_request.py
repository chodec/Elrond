from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class RequestCreate(BaseModel):
    trainer_id: uuid.UUID
    client_initial_notes: Optional[str] = None


class RequestRead(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    trainer_id: uuid.UUID

    status: str
    client_initial_notes: Optional[str] = None
    resolution_notes: Optional[str] = None

    resolved_by_user_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class TrainerResolution(BaseModel):
    resolution_notes: Optional[str] = None


class TrainerResolution(BaseModel):
    resolution_notes: Optional[str] = None
