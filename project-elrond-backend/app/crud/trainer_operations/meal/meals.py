from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from typing import Optional, List
from app.db.models import Meal

def create_meal(db: Session, meal_name: str, trainer_id: UUID) -> Meal:
    
    db_meal = Meal(
        name=meal_name,
        trainer_id=trainer_id
    )

    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    return db_meal

def read_meal(db: Session, meal_id: UUID, trainer_id: UUID) -> Optional[Meal]:
    
    db_meal = select(Meal).where(
        Meal.id == meal_id,
        Meal.trainer_id == trainer_id
    )

    statement = select(Meal).where(
        Meal.id == meal_id,
        Meal.trainer_id == trainer_id
    )

    db_meal = db.scalar(statement)

    return db_meal

def read_all_meals(
        db: Session,
        trainer_id: UUID
) -> List[Meal]:

    statement = select(Meal).where(
        Meal.trainer_id == trainer_id
    )
    
    db_exercises = db.scalars(statement).all()
    
    return db_exercises
