from pydantic import BaseModel
from typing import List

class ExerciseBase(BaseModel):
    name: str

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseRead(ExerciseBase):
    id: int

    class Config:
        from_attributes = True