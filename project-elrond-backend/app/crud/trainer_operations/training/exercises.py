from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models import Exercise as dbExercise

def create_exercise(
    db: Session, 
    exercise_name: str, 
    trainer_id: UUID
) -> dbExercise:

    db_exercise = dbExercise(
        name=exercise_name,
        trainer_id=trainer_id
    )

    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)

    return db_exercise