from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
import os
from dotenv import load_dotenv
from app.db.database import get_db
from app.schemas.meal_plan import MealPlanCreate, MealPlanRead, MealPlanUpdate
from app.crud.trainer_operations.meal.meal_plans import (
    create_meal_plan,
    read_meal_plan,
    read_meal_all_plans,
    update_meal_plan,
    delete_meal_plan,
)

router = APIRouter(tags=["Trainer Meal Plans"])

# TODO: Nahradit skutečným JWT dekódováním
def get_current_trainer_id() -> UUID:
    load_dotenv()
    return UUID(os.getenv("ID_TRAINER"))

@router.post(
    "/meal_plan",
    response_model=MealPlanRead,
    status_code=status.HTTP_201_CREATED,
    description="Create meal plan out of specific meals.",
)
def create_new_meal_plan(meal_plan_data: MealPlanCreate, db: Session = Depends(get_db)):
    try:
        return create_meal_plan(
            db=db,
            meal_plan_name=meal_plan_data.name,
            trainer_id=get_current_trainer_id(),
            meal_entries_data=meal_plan_data.meal_entries,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/meal_plan/{meal_plan_id}",
    response_model=MealPlanRead,
    description="Get specific meal plan by ID.",
)
def get_meal_plan_by_id(meal_plan_id: UUID, db: Session = Depends(get_db)):
    db_plan = read_meal_plan(
        db=db, trainer_id=get_current_trainer_id(), meal_plan_id=meal_plan_id
    )
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found or access denied."
        )
    return db_plan

@router.get(
    "/meal_plan/", 
    response_model=List[MealPlanRead], 
    description="Get all trainer's meal plans."
)
def get_all_meal_plans(
    search: Optional[str] = Query(None), 
    db: Session = Depends(get_db)
):
    # Pro seznamy vracíme [] místo 404, pokud nic nenajdeme (standard REST API)
    return read_meal_all_plans(
        db=db, search=search, trainer_id=get_current_trainer_id()
    )

@router.put(
    "/meal_plan/{meal_plan_id}",
    response_model=MealPlanRead,
    description="Update an existing meal plan. Replaces all entries.",
)
def update_existing_meal_plan(
    meal_plan_id: UUID, meal_plan_data: MealPlanUpdate, db: Session = Depends(get_db)
):
    try:
        return update_meal_plan(
            db=db,
            trainer_id=get_current_trainer_id(),
            meal_plan_id=meal_plan_id,
            plan_data=meal_plan_data,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete(
    "/meal_plan/{meal_plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete an existing meal plan.",
)
def delete_existing_meal_plan(meal_plan_id: UUID, db: Session = Depends(get_db)):
    try:
        delete_meal_plan(
            db=db, trainer_id=get_current_trainer_id(), meal_plan_id=meal_plan_id
        )
        return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        # Častá chyba: ForeignKeyConstraint (plán je už někomu přiřazen)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete plan. It might be assigned to a client. Remove assignments first."
        )