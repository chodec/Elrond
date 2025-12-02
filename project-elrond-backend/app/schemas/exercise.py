from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class ExerciseCreate(BaseModel):
    name: str


class ExerciseUpdate(BaseModel):
    name: str


class ExerciseRead(BaseModel):
    id: UUID
    name: str
    trainer_id: UUID

    class Config:
        from_attributes = True
