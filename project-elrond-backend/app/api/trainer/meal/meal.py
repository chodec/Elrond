from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import os
from dotenv import load_dotenv
from app.db.database import get_db 
from app.db.models import Meal 
from app.schemas.meal import MealCreate, Meal as MealSchema
from app.crud.trainer_operations.meal.meals import create_meal, read_meal, read_all_meals


router = APIRouter()

def get_current_trainer_id() -> UUID:
    # TODO auth
    return UUID(os.getenv("ID_TRAINER"))

@router.post(
    "/meal", 
    response_model=MealSchema,
    status_code=status.HTTP_201_CREATED
)
def create_new_meal(
    data: MealCreate, 
    db: Session = Depends(get_db)
):

    new_meal = create_meal(
        db,
        meal_name=data.name,
        trainer_id=get_current_trainer_id()
    )
    
    return new_meal

@router.get(
    "/meal/{meal_id}",
    response_model=MealSchema
)
def get_meal_by_id(
    meal_id: UUID,
    db: Session = Depends(get_db)
):
    db_plan = read_meal(
        db=db,
        meal_id=meal_id,
        trainer_id=get_current_trainer_id()
    )

    if db_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found or access denied. Ensure the provided Exercise Plan ID and Trainer ID are correct."
        )
    
    return db_plan

@router.get(
    "/meal/",
    response_model=List[MealSchema]
)
def get_all_meals(
    search: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    db_plans = read_all_meals(
        db=db,
        search=search,
        trainer_id=get_current_trainer_id()
    )

    if not db_plans:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meals not found or access denied. Make sure to create exercise plan."
        )
    
    return db_plans