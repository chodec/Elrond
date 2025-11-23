from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv
from uuid import UUID
from app.db.database import get_db 
from app.schemas.exercise_plan import ExercisePlanCreate, ExercisePlanRead
from app.crud.trainer_operations.training.exercise_plans import create_exercise_plan, read_all_exercise_plans, read_exercise_plan

router = APIRouter()

def get_current_trainer_id() -> UUID:
    # TODO auth
    return UUID(os.getenv("ID_TRAINER"))


@router.post(
    "/exercise_plan", 
    response_model = ExercisePlanRead, 
    status_code = status.HTTP_201_CREATED,
    description="Create exercise plan -> specify sets and repetition for specific exercise"
)
def create_new_exercise_plan(
    exercise_plan_data: ExercisePlanCreate,
    db: Session = Depends(get_db) 
):
    try:
        db_plan = create_exercise_plan(
            db = db,
            plan_name = exercise_plan_data.name,
            trainer_id = get_current_trainer_id(),
            notes = exercise_plan_data.notes,
            exercise_entries_data = exercise_plan_data.exercise_entries
        )
        
        return db_plan
    
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Could not create training plan."
        )
    
@router.get(
    "/exercise_plan/{exercise_plan_id}",
    response_model = ExercisePlanRead,
    description="Get specific exercise plan"
)
def get_exercise_plan_by_id(
    exercise_plan_id: UUID,
    db: Session = Depends(get_db)
):
    db_plan = read_exercise_plan(
        db = db,
        trainer_id = get_current_trainer_id(),
        exercise_plan_id = exercise_plan_id
    )

    if db_plan is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Exercise plan not found or access denied. Ensure the provided Exercise Plan ID and Trainer ID are correct."
        )
    
    return db_plan

@router.get(
    "/exercise_plan/",
    response_model = List[ExercisePlanRead],
    description="Get all exercise plans"
)
def get_all_exercise_plans(
    search: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    db_plans = read_all_exercise_plans(
        db = db,
        search = search,
        trainer_id = get_current_trainer_id()
    )

    if not db_plans:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Exercise plans not found or access denied. Make sure to create exercise plan."
        )
    
    return db_plans
