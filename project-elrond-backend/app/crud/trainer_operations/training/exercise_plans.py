from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from uuid import UUID
from typing import List, Optional
from app.db.models import (
    ExercisePlan as dbExercisePlan,
    ExercisePlanEntry as dbExercisePlanEntry,
)
from app.schemas.exercise_plan import (
    ExercisePlanEntryCreate,
    ExercisePlanEntryUpdate,
    ExercisePlanUpdate,
)


def create_exercise_plan(
    db: Session,
    plan_name: str,
    trainer_id: UUID,
    notes: str | None,
    exercise_entries_data: List[ExercisePlanEntryCreate],
) -> dbExercisePlan:

    db_exercise_plan = dbExercisePlan(
        name=plan_name, trainer_id=trainer_id, notes=notes
    )

    db.add(db_exercise_plan)
    db.flush()

    for entry_data in exercise_entries_data:
        db_entry = dbExercisePlanEntry(
            exercise_plan_id=db_exercise_plan.id,
            base_exercise_id=entry_data.base_exercise_id,
            sets=entry_data.sets,
            repetitions=entry_data.repetitions,
            day_of_week=entry_data.day_of_week,
            order_in_session=entry_data.order_in_session,
            notes=entry_data.notes,
        )
        db.add(db_entry)

    db.commit()
    db.refresh(db_exercise_plan)

    return db_exercise_plan


def read_exercise_plan(
    db: Session, trainer_id: UUID, exercise_plan_id: UUID
) -> Optional[dbExercisePlan]:

    statement = select(dbExercisePlan).where(
        dbExercisePlan.id == exercise_plan_id, dbExercisePlan.trainer_id == trainer_id
    )

    db_exercise_plan = db.scalar(statement)

    return db_exercise_plan


def read_all_exercise_plans(
    db: Session, trainer_id: UUID, search: Optional[str] = None
) -> List[dbExercisePlan]:

    statement = select(dbExercisePlan).where(dbExercisePlan.trainer_id == trainer_id)

    if search:
        statement = statement.where(dbExercisePlan.name.ilike(f"%{search}%"))

    db_exercise_plans = db.scalars(statement).all()

    return db_exercise_plans


def update_exercise_plan(
    db: Session, trainer_id: UUID, exercise_plan_id: UUID, plan_data: ExercisePlanUpdate
) -> Optional[dbExercisePlan]:

    db_exercise_plan = read_exercise_plan(db, trainer_id, exercise_plan_id)

    if not db_exercise_plan:
        return None

    db_exercise_plan.name = plan_data.name
    db_exercise_plan.notes = plan_data.notes

    delete_statement = delete(dbExercisePlanEntry).where(
        dbExercisePlanEntry.exercise_plan_id == exercise_plan_id
    )
    db.execute(delete_statement)

    for entry_data in plan_data.exercise_entries:
        db_entry = dbExercisePlanEntry(
            exercise_plan_id=db_exercise_plan.id,
            base_exercise_id=entry_data.base_exercise_id,
            sets=entry_data.sets,
            repetitions=entry_data.repetitions,
            day_of_week=entry_data.day_of_week,
            order_in_session=entry_data.order_in_session,
            notes=entry_data.notes,
        )
        db.add(db_entry)

    db.commit()
    db.refresh(db_exercise_plan)

    return db_exercise_plan


def delete_exercise_plan(db: Session, trainer_id: UUID, exercise_plan_id: UUID) -> bool:

    db_exercise_plan = read_exercise_plan(db, trainer_id, exercise_plan_id)

    if not db_exercise_plan:
        return False

    delete_entries_statement = delete(dbExercisePlanEntry).where(
        dbExercisePlanEntry.exercise_plan_id == exercise_plan_id
    )
    db.execute(delete_entries_statement)

    db.delete(db_exercise_plan)
    db.commit()

    return True
