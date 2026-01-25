from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, exc
from uuid import UUID
from typing import List

from app.db.models import (
    MealPlanAssignment,
    MealPlan,
    ExercisePlanAssignment,
    ExercisePlan,
)
from app.crud.trainer_operations.subscriptions.client_subscription_validation import (
    is_client_subscription_active,
)

class AssignmentError(Exception):
    pass

def create_meal_plan_assignment(
    db: Session, client_id: UUID, trainer_id: UUID, meal_plan_id: UUID
) -> MealPlanAssignment:
    if not is_client_subscription_active(db, client_id, trainer_id):
        raise AssignmentError(
            "Client does not have an active and valid subscription with this trainer."
        )

    try:
        db_assignment = MealPlanAssignment(client_id=client_id, meal_plan_id=meal_plan_id)
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        return db_assignment
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during meal plan assignment: {str(e)}")

def read_client_meal_assignments(db: Session, client_id: UUID) -> List[MealPlan]:
    statement = (
        select(MealPlan)
        .join(MealPlanAssignment, MealPlan.id == MealPlanAssignment.meal_plan_id)
        .where(MealPlanAssignment.client_id == client_id)
        .options(joinedload(MealPlan.meal_entries))
    )
    return db.scalars(statement).unique().all()

def create_exercise_plan_assignment(
    db: Session, client_id: UUID, trainer_id: UUID, exercise_plan_id: UUID
) -> ExercisePlanAssignment:
    if not is_client_subscription_active(db, client_id, trainer_id):
        raise AssignmentError(
            "Client does not have an active and valid subscription with this trainer."
        )

    try:
        db_assignment = ExercisePlanAssignment(
            client_id=client_id, exercise_plan_id=exercise_plan_id
        )
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        return db_assignment
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error during exercise plan assignment: {str(e)}")

def read_client_exercise_assignments(
    db: Session, client_id: UUID
) -> List[ExercisePlan]:
    statement = (
        select(ExercisePlan)
        .join(
            ExercisePlanAssignment,
            ExercisePlan.id == ExercisePlanAssignment.exercise_plan_id,
        )
        .where(ExercisePlanAssignment.client_id == client_id)
        .options(joinedload(ExercisePlan.exercise_entries))
    )
    return db.scalars(statement).unique().all()