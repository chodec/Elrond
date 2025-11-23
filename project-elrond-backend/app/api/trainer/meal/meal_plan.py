from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
import os
from dotenv import load_dotenv
from app.db.database import get_db 
from app.schemas.meal_plan import MealPlanCreate, MealPlanRead
from app.crud.trainer_operations.meal.meal_plans import create_meal_plan, read_meal_plan, read_meal_all_plans

router = APIRouter()

def get_current_trainer_id() -> UUID:
    # TODO auth
    return UUID(os.getenv("ID_TRAINER"))

@router.post(
    "/meal_plan", 
    response_model = MealPlanRead, 
    status_code = status.HTTP_201_CREATED,
    description="Create meal plan out of specific meals, set specific nutrition score"
)
def create_new_meal_plan(
    meal_plan_data: MealPlanCreate, 
    db: Session = Depends(get_db) 
):
    db_plan = create_meal_plan(
        db = db,
        meal_plan_name = meal_plan_data.name,
        trainer_id = get_current_trainer_id(),
        meal_entries_data = meal_plan_data.meal_entries
    )
    
    return db_plan

@router.get(
    "/meal_plan/{meal_plan_id}",
    response_model = MealPlanRead,
    description="Get specific meal plan by ID"
)
def get_meal_plan_by_id(
    meal_plan_id:UUID,
    db:Session = Depends(get_db)
):

    db_plan = read_meal_plan(
        db = db,
        trainer_id = get_current_trainer_id(),
        meal_plan_id = meal_plan_id
    )

    if db_plan is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Meal plan not found or access denied. Ensure the provided Meal Plan ID and Trainer ID are correct."
        )
    
    return db_plan

@router.get(
    "/meal_plan/",
    response_model = List[MealPlanRead],
    description="Get all meal plans"
)
def get_all_meal_plans(
    search: Optional[str] = None, 
    db:Session = Depends(get_db)
):

    db_plan = read_meal_all_plans(
        db = db,
        search = search,
        trainer_id = get_current_trainer_id()
    )

    if not db_plan:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Meal plans not found or access denied. Make sure to create meal plan."
        )
    
    return db_plan