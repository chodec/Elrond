from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db 
from app.schemas.exercise import ExerciseRead, ExerciseCreateWithOwner
from app.crud.trainer_operations.training.exercises import create_exercise

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
