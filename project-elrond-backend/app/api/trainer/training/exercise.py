from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from typing import List, Optional
from uuid import UUID
from app.db.database import get_db 
from app.schemas.exercise import ExerciseRead, ExerciseCreate
from app.crud.trainer_operations.training.exercises import create_exercise, read_exercise, read_all_exercises

router = APIRouter()

def get_current_trainer_id() -> UUID:
    # TODO auth
    return UUID(os.getenv("ID_TRAINER"))

@router.post(
    "/exercise", 
    response_model = ExerciseRead,
    status_code = status.HTTP_201_CREATED,
    description="Create exercesi for exercise plans -> sets etc. will be specified in the exercise plans"
)
def create_new_exercise(
    data: ExerciseCreate,
    db: Session = Depends(get_db)
):  
    
    try:
        print(get_current_trainer_id())
        new_exercise = create_exercise(
            db, 
            exercise_name = data.name, 
            trainer_id = get_current_trainer_id()
        )
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Creating exercise failed."
        )

    return new_exercise

@router.get(
    "/exercise/{exercise_id}",
    response_model = ExerciseRead,
    description="Get specific exercise by ID"
)
def get_exercise_by_id(
    exercise_id: UUID,
    db: Session = Depends(get_db)
):
    db_plan = read_exercise(
        db = db,
        exercise_id = exercise_id,
        trainer_id = get_current_trainer_id()
    )

    if db_plan is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Exercise not found or access denied. Ensure the provided Exercise Plan ID and Trainer ID are correct."
        )
    
    return db_plan

@router.get(
    "/exercise/",
    response_model = List[ExerciseRead],
    description="Get all exercise"
)
def get_all_exercises(
    search: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    db_exercise = read_all_exercises(
        db = db,
        search = search,
        trainer_id = get_current_trainer_id()
    )

    if not db_exercise:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Exercises not found or access denied. Make sure to create exercise plan."
        )
    
    return db_exercise