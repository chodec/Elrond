from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import Optional, List
from uuid import UUID
from app.db.models import Exercise
from app.schemas.exercise import ExerciseUpdate

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

def read_exercise(
        db: Session,
        exercise_id: UUID,
        trainer_id: UUID
        ) -> Optional[Exercise]:

    statement = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.trainer_id == trainer_id
    )

    db_exercise = db.scalar(statement)

    return db_exercise

def read_all_exercises(
        db: Session,
        trainer_id: UUID,
        search: Optional[str] = None
) -> List[Exercise]:

    statement = select(Exercise).where(
        Exercise.trainer_id == trainer_id
    )

    if search:
        statement = statement.where(
            Exercise.name.ilike(f"%{search}%")
        )
    
    db_exercises = db.scalars(statement).all()
    
    return db_exercises

def update_exercise(
        db: Session,
        exercise_id: UUID,
        trainer_id: UUID,
        data: ExerciseUpdate
) -> Optional[Exercise]:
    
    db_exercise = read_exercise(db, exercise_id, trainer_id)
    
    if not db_exercise:
        return None  

    # Aktualizace dat
    db_exercise.name = data.name
    
    db.commit()
    db.refresh(db_exercise)
    
    return db_exercise

def delete_exercise(
        db: Session,
        exercise_id: UUID,
        trainer_id: UUID
) -> bool:
    
    db_exercise = read_exercise(db, exercise_id, trainer_id)
    
    if not db_exercise:
        return False  

    db.delete(db_exercise)
    db.commit()
    
    return True