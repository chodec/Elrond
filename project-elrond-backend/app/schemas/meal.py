from pydantic import BaseModel
from uuid import UUID


class MealCreate(BaseModel):
    name: str


class MealUpdate(BaseModel):
    name: str


class Meal(BaseModel):
    id: UUID
    name: str
    trainer_id: UUID

    class Config:
        from_attributes = True
