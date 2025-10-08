from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db 
from app.db.models import Meal 
from app.schemas.meal import MealCreate, MealCreateWithOwner, Meal as MealSchema
from app.crud.trainer_operations.meal.meals import create_meal


router = APIRouter()

@router.post(
    "/meal", 
    response_model=MealSchema,
    status_code=status.HTTP_201_CREATED
)
def create_new_meal(
    data: MealCreateWithOwner, 
    db: Session = Depends(get_db)
):

    new_meal = create_meal(db, meal_name=data.name, trainer_id=data.trainer_id)
    
    return new_meal