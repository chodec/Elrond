from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import os
from dotenv import load_dotenv

from app.db.database import get_db
from app.crud.trainer_operations.assignments.assignments import (
    create_meal_plan_assignment,
    create_exercise_plan_assignment,
    AssignmentError,
)
from app.schemas.assignment import AssignmentCreate

# TODO: Nahradit skutečným JWT dekódováním
def get_current_trainer_id() -> UUID:
    load_dotenv()
    return UUID(os.getenv("ID_TRAINER"))

router = APIRouter(tags=["Trainer Assignments"])

@router.post(
    "/assignments/meal-plan",
    status_code=status.HTTP_201_CREATED,
    description="Assign a meal plan to a client who has an active subscription.",
)
def assign_meal_plan_to_client(
    assignment_data: AssignmentCreate,
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db),
):
    if not assignment_data.meal_plan_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Meal plan ID is required."
        )

    try:
        db_assignment = create_meal_plan_assignment(
            db=db,
            client_id=assignment_data.client_id,
            trainer_id=trainer_id,
            meal_plan_id=assignment_data.meal_plan_id,
        )

        return {
            "message": "Meal plan successfully assigned.",
            "assignment_id": db_assignment.id,
        }

    except AssignmentError as e:
        # 403 Forbidden je správně - trenér se snaží o akci, na kterou klient nemá "právo" (předplatné)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/assignments/exercise-plan",
    status_code=status.HTTP_201_CREATED,
    description="Assign an exercise plan to a client who has an active subscription.",
)
def assign_exercise_plan_to_client(
    assignment_data: AssignmentCreate,
    trainer_id: UUID = Depends(get_current_trainer_id),
    db: Session = Depends(get_db),
):
    if not assignment_data.exercise_plan_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Exercise plan ID is required."
        )

    try:
        db_assignment = create_exercise_plan_assignment(
            db=db,
            client_id=assignment_data.client_id,
            trainer_id=trainer_id,
            exercise_plan_id=assignment_data.exercise_plan_id,
        )

        return {
            "message": "Exercise plan successfully assigned.",
            "assignment_id": db_assignment.id,
        }

    except AssignmentError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))