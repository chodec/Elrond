from pydantic import BaseModel
from uuid import UUID

class ExerciseCreate(BaseModel):
    name: str

class ExerciseRead(BaseModel):
    id: UUID
    name: str
    trainer_id: UUID 
    
    class Config:
        # Can read ORM model
        from_attributes = True
