from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.meal import Meal, MealCreate
from app.db.models import Trainer, Meal

def create_meal(db: Session, meal_name: str, trainer_id: UUID) -> Meal:
    
    db_meal = Meal(
        name=meal_name,
        trainer_id=trainer_id
    )

    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    return db_meal