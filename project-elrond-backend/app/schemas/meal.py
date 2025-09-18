from pydantic import BaseModel
from typing import Optional

class MealBase(BaseModel):
    name: str

class MealCreate(MealBase):
    pass

class MealRead(MealBase):
    id: int

    class Config:
        from_attributes = True