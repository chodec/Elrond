from pydantic import BaseModel
from typing import List, Optional
import uuid 

class MealPlanEntryCreate(BaseModel):
    base_meal_id: uuid.UUID 
    serving_size_grams: int
    time_slot: str
    notes: Optional[str] = None

    carbohydrates_g: int 
    fat_g: int          
    protein_g: int

class MealPlanEntryUpdate(MealPlanEntryCreate):
    pass

class MealPlanUpdate(BaseModel):
    name: str
    meal_entries: List[MealPlanEntryUpdate] 

class MealPlanCreate(BaseModel):
    name: str
    meal_entries: List[MealPlanEntryCreate] 

class MealPlanEntryRead(MealPlanEntryCreate):
    id: uuid.UUID
    
class MealPlanRead(MealPlanCreate):
    id: uuid.UUID
    meal_entries: List[MealPlanEntryRead] 

    class Config:
        from_attributes = True