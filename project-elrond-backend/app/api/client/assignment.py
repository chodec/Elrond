# app/api/endpoints/client_plans.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import os
from dotenv import load_dotenv

from app.db.database import get_db 
from app.crud.trainer_operations.assignments.assignments import read_client_meal_assignments, read_client_exercise_assignments
from app.schemas.meal_plan import MealPlanRead 
from app.schemas.exercise_plan import ExercisePlanRead

def get_current_client_id() -> UUID:
    # TODO: jwt
    load_dotenv() 
    return UUID(os.getenv("ID_CLIENT"))

router = APIRouter()


@router.get(
    "/assignments/meal-plans",
    response_model = List[MealPlanRead]
)
def get_my_meal_plans(
    client_id: UUID = Depends(get_current_client_id),
    db: Session = Depends(get_db)
):
    db_plans = read_client_meal_assignments(
        db = db,
        client_id = client_id
    )

    if not db_plans:
        return []
    
    return db_plans


@router.get(
    "/assignments/exercise-plans",
    response_model = List[ExercisePlanRead]
)
def get_my_exercise_plans(
    client_id: UUID = Depends(get_current_client_id),
    db: Session = Depends(get_db)
):
    db_plans = read_client_exercise_assignments(
        db = db,
        client_id = client_id
    )
    
    if not db_plans:
        return []
        
    return db_plans