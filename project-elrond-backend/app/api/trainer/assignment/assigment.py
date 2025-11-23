from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import os
from dotenv import load_dotenv

from app.db.database import get_db

from app.crud.trainer_operations.assignments.assignments import (
    create_meal_plan_assignment, 
    create_exercise_plan_assignment, 
    AssignmentError
)
from app.schemas.assignment import AssignmentCreate 

def get_current_trainer_id() -> UUID:
    # TODO jwt
    load_dotenv() 
    return UUID(os.getenv("ID_TRAINER"))

router = APIRouter()


@router.post(
    "/assignments/meal-plan", 
    status_code=status.HTTP_201_CREATED,
    description="Assign meal plan to the subscribed client"
)
def assign_meal_plan_to_client(
    assignment_data: AssignmentCreate,
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db)
):
    if not assignment_data.meal_plan_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        db_assignment = create_meal_plan_assignment(
            db=db,
            client_id=assignment_data.client_id,
            trainer_id=trainer_id,
            meal_plan_id=assignment_data.meal_plan_id
        )
        
        return {
            "message": "Meal plan successfully assigned to client.",
            "assignment_id": db_assignment.id
        }
        
    except AssignmentError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post(
    "/assignments/exercise-plan", 
    status_code=status.HTTP_201_CREATED,
    description="Assign exercise plan to the subscribed client"
)
def assign_exercise_plan_to_client(
    assignment_data: AssignmentCreate,
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db)
):
    if not assignment_data.exercise_plan_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        db_assignment = create_exercise_plan_assignment(
            db=db,
            client_id=assignment_data.client_id,
            trainer_id=trainer_id,
            exercise_plan_id=assignment_data.exercise_plan_id
        )
        
        return {
            "message": "Exercise plan successfully assigned to client.",
            "assignment_id": db_assignment.id
        }
        
    except AssignmentError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )