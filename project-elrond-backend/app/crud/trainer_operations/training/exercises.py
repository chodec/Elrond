from sqlalchemy.orm import Session
from sqlalchemy import select, delete, exc
from typing import Optional, List
from uuid import UUID
from app.db.models import Exercise
from app.schemas.exercise import ExerciseUpdate


def create_exercise(db: Session, exercise_name: str, trainer_id: UUID) -> Exercise:
    try:
        db_exercise = Exercise(name=exercise_name, trainer_id=trainer_id)
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        return db_exercise
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during exercise creation: {str(e)}")


def read_exercise(
    db: Session, exercise_id: UUID, trainer_id: UUID
) -> Optional[Exercise]:
    statement = select(Exercise).where(
        Exercise.id == exercise_id, Exercise.trainer_id == trainer_id
    )
    return db.scalar(statement)


def read_all_exercises(
    db: Session, trainer_id: UUID, search: Optional[str] = None
) -> List[Exercise]:
    statement = select(Exercise).where(Exercise.trainer_id == trainer_id)

    if search:
        statement = statement.where(Exercise.name.ilike(f"%{search}%"))

    return list(db.scalars(statement).all())


def update_exercise(
    db: Session, exercise_id: UUID, trainer_id: UUID, data: ExerciseUpdate
) -> Exercise:
    db_exercise = read_exercise(db, exercise_id, trainer_id)

    if not db_exercise:
        raise ValueError("Exercise not found")

    try:
        db_exercise.name = data.name
        db.commit()
        db.refresh(db_exercise)
        return db_exercise
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during exercise update: {str(e)}")


def delete_exercise(db: Session, exercise_id: UUID, trainer_id: UUID) -> UUID:
    db_exercise = read_exercise(db, exercise_id, trainer_id)

    if not db_exercise:
        raise ValueError("Exercise not found")

    try:
        db.delete(db_exercise)
        db.commit()
        return exercise_id
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during exercise deletion: {str(e)}")