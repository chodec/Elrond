from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import os
from dotenv import load_dotenv

from app.db.database import get_db
from app.crud.trainer_operations.assignments.assignments import (
    read_client_meal_assignments,
    read_client_exercise_assignments,
)
from app.schemas.meal_plan import MealPlanRead
from app.schemas.exercise_plan import ExercisePlanRead

# TODO: Replace with proper JWT authentication dependency later
def get_current_client_id() -> UUID:
    load_dotenv()
    return UUID(os.getenv("ID_CLIENT"))

router = APIRouter(tags=["Client Assignments"])

@router.get(
    "/assignments/meal-plans",
    response_model=List[MealPlanRead],
    description="Get meal plans assigned to the current client by their trainer.",
)
def get_my_meal_plans(
    client_id: UUID = Depends(get_current_client_id), 
    db: Session = Depends(get_db)
):
    return read_client_meal_assignments(db=db, client_id=client_id)

@router.get(
    "/assignments/exercise-plans",
    response_model=List[ExercisePlanRead],
    description="Get exercise plans assigned to the current client by their trainer.",
)
def get_my_exercise_plans(
    client_id: UUID = Depends(get_current_client_id), 
    db: Session = Depends(get_db)
):
    return read_client_exercise_assignments(db=db, client_id=client_id)