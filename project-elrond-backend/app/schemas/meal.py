from pydantic import BaseModel
from uuid import UUID

class MealCreate(BaseModel):
    name: str

class Meal(BaseModel):
    id: UUID
    name: str
    
    class Config:
        from_attributes = True
