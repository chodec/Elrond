from pydantic import BaseModel
from typing import List, Optional

class MealPlanBase(BaseModel):
    name: str

class MealPlanCreate(MealPlanBase):
    meals: List[int]

class MealPlanRead(MealPlanBase):
    id: int
    trainer_id: int
    meals: List[int]

    class Config:
        from_attributes = True