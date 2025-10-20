from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from uuid import UUID
from app.db.models import Exercise

def create_exercise(
    db: Session, 
    exercise_name: str, 
    trainer_id: UUID
) -> Exercise:

    db_exercise = Exercise(
        name=exercise_name,
        trainer_id=trainer_id
    )

    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)

    return db_exercise

def read_exercise(db: Session, exercise_id: UUID, trainer_id: UUID) -> Optional[Exercise]:
    
    db_meal = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.trainer_id == trainer_id
    )

    statement = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.trainer_id == trainer_id
    )

    db_meal = db.scalar(statement)

    return db_meal

def read_all_exercises(
        db: Session,
        trainer_id: UUID
) -> List[Exercise]:

    statement = select(Exercise).where(
        Exercise.trainer_id == trainer_id
    )
    
    db_exercises = db.scalars(statement).all()
    
    return db_exercises