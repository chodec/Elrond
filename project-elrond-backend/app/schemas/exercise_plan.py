from pydantic import BaseModel
from typing import List

class ExercisePlanBase(BaseModel):
    name: str
    trainer_id: int
    meals: List[int]

class ExercisePlanCreate(ExercisePlanBase):
    pass

class ExercisePlanRead(ExercisePlanBase):
    id: int

    class Config:
        from_attributes = True
