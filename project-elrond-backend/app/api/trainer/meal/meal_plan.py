from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db 
from app.schemas.meal_plan import MealPlanCreate, MealPlanRead
from app.crud.trainer_operations.meal.meal_plans import create_meal_plan 

router = APIRouter()


@router.post(
    "/meal_plan", 
    response_model=MealPlanRead, 
    status_code=status.HTTP_201_CREATED
)
def create_new_meal_plan_endpoint(
    meal_plan_data: MealPlanCreate, 
    
    db: Session = Depends(get_db) 
):
    db_plan = create_meal_plan(
        db=db,
        meal_plan_name=meal_plan_data.name,
        trainer_id=meal_plan_data.trainer_id,
        meal_entries_data=meal_plan_data.meal_entries
    )
    
    return db_plan