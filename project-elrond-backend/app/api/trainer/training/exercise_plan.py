from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db 
from app.schemas.exercise_plan import ExercisePlanCreate, ExercisePlanRead
from app.crud.trainer_operations.training.exercise_plans import create_exercise_plan

router = APIRouter()

@router.post(
    "/exercise_plan", 
    response_model=ExercisePlanRead, 
    status_code=status.HTTP_201_CREATED
)
def create_new_exercise_plan_endpoint(
    exercise_plan_data: ExercisePlanCreate,
    db: Session = Depends(get_db) 
):
    try:
        db_plan = create_exercise_plan(
            db=db,
            plan_name=exercise_plan_data.name,
            trainer_id=exercise_plan_data.trainer_id,
            notes=exercise_plan_data.notes,
            exercise_entries_data=exercise_plan_data.exercise_entries
        )
        
        return db_plan
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create training plan."
        )
