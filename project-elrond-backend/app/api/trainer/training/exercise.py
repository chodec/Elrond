from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import os
from dotenv import load_dotenv
from app.db.database import get_db
from app.schemas.exercise import ExerciseRead, ExerciseCreate, ExerciseUpdate
from app.crud.trainer_operations.training.exercises import (
    create_exercise,
    read_exercise,
    read_all_exercises,
    update_exercise,
    delete_exercise,
)

router = APIRouter(tags=["Trainer Exercises"])

# TODO: Replace with JWT auth dependency
def get_current_trainer_id() -> UUID:
    load_dotenv()
    return UUID(os.getenv("ID_TRAINER"))

@router.post(
    "/exercise",
    response_model=ExerciseRead,
    status_code=status.HTTP_201_CREATED,
    description="Create a base exercise for your exercise plans.",
)
def create_new_exercise(data: ExerciseCreate, db: Session = Depends(get_db)):
    try:
        return create_exercise(
            db, 
            exercise_name=data.name, 
            trainer_id=get_current_trainer_id()
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/exercise/{exercise_id}",
    response_model=ExerciseRead,
    description="Get specific exercise by ID.",
)
def get_exercise_by_id(exercise_id: UUID, db: Session = Depends(get_db)):
    db_exercise = read_exercise(
        db=db, exercise_id=exercise_id, trainer_id=get_current_trainer_id()
    )

    if not db_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found or access denied."
        )

    return db_exercise

@router.get(
    "/exercise/", 
    response_model=List[ExerciseRead], 
    description="Get all base exercises created by the trainer."
)
def get_all_exercises(
    search: Optional[str] = Query(None), 
    db: Session = Depends(get_db)
):
    # Standard: vracíme prázdný seznam [], pokud nic nenalezneme
    return read_all_exercises(
        db=db, search=search, trainer_id=get_current_trainer_id()
    )

@router.put(
    "/exercise/{exercise_id}",
    response_model=ExerciseRead,
    description="Update an existing exercise name.",
)
def update_existing_exercise(
    exercise_id: UUID, data: ExerciseUpdate, db: Session = Depends(get_db)
):
    try:
        return update_exercise(
            db=db,
            exercise_id=exercise_id,
            trainer_id=get_current_trainer_id(),
            data=data,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete(
    "/exercise/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete an existing exercise.",
)
def delete_existing_exercise(exercise_id: UUID, db: Session = Depends(get_db)):
    try:
        delete_exercise(
            db=db, exercise_id=exercise_id, trainer_id=get_current_trainer_id()
        )
        return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        # Zachycení Foreign Key constraint - cvik je součástí nějakého plánu
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete exercise. It is currently used in one or more exercise plans."
        )