from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.db.database import get_db 
from app.schemas.exercise import ExerciseRead, ExerciseCreateWithOwner
from app.crud.trainer_operations.training.exercises import create_exercise, read_exercise, read_all_exercises

router = APIRouter()

@router.post(
    "/exercise", 
    response_model=ExerciseRead,
    status_code=status.HTTP_201_CREATED
)
def create_new_exercise(
    data: ExerciseCreateWithOwner,
    db: Session = Depends(get_db)
):  
    
    try:
        new_exercise = create_exercise(
            db, 
            exercise_name=data.name, 
            trainer_id=data.trainer_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Creating exercise failed."
        )

    return new_exercise

@router.get(
    "/exercise/{exercise_id}",
    response_model=ExerciseRead
)
def get_exercise_by_id(
    exercise_id: UUID,
    trainer_id: UUID, 
    db: Session = Depends(get_db)
):
    db_plan = read_exercise(
        db=db,
        exercise_id=exercise_id,
        trainer_id=trainer_id
    )

    if db_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found or access denied. Ensure the provided Exercise Plan ID and Trainer ID are correct."
        )
    
    return db_plan

@router.get(
    "/exercise/",
    response_model=List[ExerciseRead]
)
def get_all_exercises(
    trainer_id: UUID,
    search: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    db_exercise = read_all_exercises(
        db=db,
        search=search,
        trainer_id=trainer_id
    )

    if not db_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercises not found or access denied. Make sure to create exercise plan."
        )
    
    return db_exercise