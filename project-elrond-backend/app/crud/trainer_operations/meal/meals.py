from sqlalchemy.orm import Session
from sqlalchemy import select, delete, exc
from uuid import UUID
from typing import Optional, List
from app.db.models import Meal
from app.schemas.meal import MealUpdate


def create_meal(db: Session, meal_name: str, trainer_id: UUID) -> Meal:
    try:
        db_meal = Meal(name=meal_name, trainer_id=trainer_id)
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
        return db_meal
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during meal creation: {str(e)}")


def read_meal(db: Session, meal_id: UUID, trainer_id: UUID) -> Optional[Meal]:
    statement = select(Meal).where(Meal.id == meal_id, Meal.trainer_id == trainer_id)
    return db.scalar(statement)


def read_all_meals(
    db: Session, trainer_id: UUID, search: Optional[str] = None
) -> List[Meal]:
    statement = select(Meal).where(Meal.trainer_id == trainer_id)

    if search:
        statement = statement.where(Meal.name.ilike(f"%{search}%"))

    return list(db.scalars(statement).all())


def update_meal(
    db: Session, meal_id: UUID, trainer_id: UUID, data: MealUpdate
) -> Meal:
    db_meal = read_meal(db, meal_id, trainer_id)

    if not db_meal:
        raise ValueError("Meal not found")

    try:
        db_meal.name = data.name
        db.commit()
        db.refresh(db_meal)
        return db_meal
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during meal update: {str(e)}")


def delete_meal(db: Session, meal_id: UUID, trainer_id: UUID) -> UUID:
    db_meal = read_meal(db, meal_id, trainer_id)

    if not db_meal:
        raise ValueError("Meal not found")

    try:
        db.delete(db_meal)
        db.commit()
        return meal_id
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during meal deletion: {str(e)}")