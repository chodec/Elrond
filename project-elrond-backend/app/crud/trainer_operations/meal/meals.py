from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from uuid import UUID
from typing import Optional, List
from app.db.models import Meal
from app.schemas.meal import MealUpdate


def create_meal(db: Session, meal_name: str, trainer_id: UUID) -> Meal:

    db_meal = Meal(name=meal_name, trainer_id=trainer_id)

    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    return db_meal


def read_meal(db: Session, meal_id: UUID, trainer_id: UUID) -> Optional[Meal]:

    db_meal = select(Meal).where(Meal.id == meal_id, Meal.trainer_id == trainer_id)

    statement = select(Meal).where(Meal.id == meal_id, Meal.trainer_id == trainer_id)

    db_meal = db.scalar(statement)

    return db_meal


def read_all_meals(
    db: Session, trainer_id: UUID, search: Optional[str] = None
) -> List[Meal]:

    statement = select(Meal).where(Meal.trainer_id == trainer_id)

    if search:
        statement = statement.where(Meal.name.ilike(f"%{search}%"))

    db_meals = db.scalars(statement).all()

    return db_meals


def update_meal(
    db: Session, meal_id: UUID, trainer_id: UUID, data: MealUpdate
) -> Optional[Meal]:

    db_meal = read_meal(db, meal_id, trainer_id)

    if not db_meal:
        return None

    db_meal.name = data.name

    db.commit()
    db.refresh(db_meal)

    return db_meal


def delete_meal(db: Session, meal_id: UUID, trainer_id: UUID) -> bool:

    db_meal = read_meal(db, meal_id, trainer_id)

    if not db_meal:
        return False

    db.delete(db_meal)
    db.commit()

    return True
