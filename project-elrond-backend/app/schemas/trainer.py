from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class TrainerUpdate(BaseModel):
    specialization: Optional[str] = None


class Trainer(BaseModel):
    user_id: UUID
    specialization: str | None = None

    class Config:
        from_attributes = True
