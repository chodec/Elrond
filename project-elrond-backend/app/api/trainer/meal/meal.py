from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import os
from dotenv import load_dotenv
from app.db.database import get_db
from app.schemas.meal import MealCreate, Meal as MealSchema, MealUpdate
from app.crud.trainer_operations.meal.meals import (
    create_meal,
    read_meal,
    read_all_meals,
    update_meal,
    delete_meal,
)

router = APIRouter(tags=["Trainer Meals"])

# TODO: Nahradit skutečným JWT dekódováním
def get_current_trainer_id() -> UUID:
    load_dotenv()
    return UUID(os.getenv("ID_TRAINER"))

@router.post(
    "/meal",
    response_model=MealSchema,
    status_code=status.HTTP_201_CREATED,
    description="Create a base meal that can be added to meal plans.",
)
def create_new_meal(data: MealCreate, db: Session = Depends(get_db)):
    try:
        return create_meal(db, meal_name=data.name, trainer_id=get_current_trainer_id())
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/meal/{meal_id}", 
    response_model=MealSchema, 
    description="Get specific meal by ID."
)
def get_meal_by_id(meal_id: UUID, db: Session = Depends(get_db)):
    db_meal = read_meal(db=db, meal_id=meal_id, trainer_id=get_current_trainer_id())
    
    if not db_meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found or access denied."
        )
    return db_meal

@router.get(
    "/meal/", 
    response_model=List[MealSchema], 
    description="Get all meals created by the trainer."
)
def get_all_meals(
    search: Optional[str] = Query(None), 
    db: Session = Depends(get_db)
):
    # Opět: pro prázdné výsledky vracíme 200 OK [], ne 404.
    return read_all_meals(db=db, search=search, trainer_id=get_current_trainer_id())

@router.put(
    "/meal/{meal_id}", 
    response_model=MealSchema, 
    description="Update an existing meal's name."
)
def update_existing_meal(
    meal_id: UUID, 
    data: MealUpdate, 
    db: Session = Depends(get_db)
):
    try:
        return update_meal(
            db=db, 
            meal_id=meal_id, 
            trainer_id=get_current_trainer_id(), 
            data=data
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete(
    "/meal/{meal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete an existing meal.",
)
def delete_existing_meal(meal_id: UUID, db: Session = Depends(get_db)):
    try:
        delete_meal(db=db, meal_id=meal_id, trainer_id=get_current_trainer_id())
        return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        # Tady zachycujeme pokus o smazání jídla, které je v jídelníčku (FK constraint)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete meal. It is currently part of one or more meal plans."
        )