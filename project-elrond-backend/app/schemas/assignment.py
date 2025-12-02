from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class AssignmentCreate(BaseModel):
    client_id: UUID
    meal_plan_id: Optional[UUID] = None
    exercise_plan_id: Optional[UUID] = None
