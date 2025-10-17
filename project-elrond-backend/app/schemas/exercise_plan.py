from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ExercisePlanEntryCreate(BaseModel):
    base_exercise_id: UUID 
    
    sets: int            
    repetitions: str         
    
    day_of_week: str
    order_in_session: int 
    
    notes: Optional[str] = None 

class ExercisePlanCreate(BaseModel):
    name: str
    trainer_id: UUID 
    
    notes: Optional[str] = None 
    
    exercise_entries: List[ExercisePlanEntryCreate] 

class ExercisePlanEntryRead(ExercisePlanEntryCreate):
    id: UUID
    
class ExercisePlanRead(ExercisePlanCreate):
    id: UUID
    exercise_entries: List[ExercisePlanEntryRead] 

    class Config:
        from_attributes = True