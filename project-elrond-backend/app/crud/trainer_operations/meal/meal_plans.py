from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.schemas.meal_plan import MealPlanEntryCreate, MealPlanUpdate
from uuid import UUID
from app.db.models import MealPlan, MealPlanEntry
from typing import List, Optional


def create_meal_plan(
    db: Session,
    meal_plan_name: str,
    trainer_id: UUID,
    meal_entries_data: List[MealPlanEntryCreate],
) -> MealPlan:

    db_meal_plan = MealPlan(name=meal_plan_name, trainer_id=trainer_id)
    db.add(db_meal_plan)
    db.flush()

    for entry_data in meal_entries_data:
        db_entry = MealPlanEntry(
            meal_plan_id=db_meal_plan.id,
            base_meal_id=entry_data.base_meal_id,
            serving_size_grams=entry_data.serving_size_grams,
            time_slot=entry_data.time_slot,
            notes=entry_data.notes,
            carbohydrates_g=entry_data.carbohydrates_g,
            fat_g=entry_data.fat_g,
            protein_g=entry_data.protein_g,
        )
        db.add(db_entry)

    db.commit()
    db.refresh(db_meal_plan)

    return db_meal_plan


def read_meal_plan(
    db: Session, trainer_id: UUID, meal_plan_id: UUID
) -> Optional[MealPlan]:  # mealplan could not exists

    statement = select(MealPlan).where(
        MealPlan.id == meal_plan_id, MealPlan.trainer_id == trainer_id
    )

    db_meal_plan = db.scalar(statement)  # scalar returns one line

    return db_meal_plan


def read_meal_all_plans(
    db: Session, trainer_id: UUID, search: Optional[str] = None
) -> List[MealPlan]:

    statement = select(MealPlan).where(MealPlan.trainer_id == trainer_id)

    if search:
        statement = statement.where(MealPlan.name.ilike(f"%{search}%"))

    db_meal_plans = db.scalars(statement).all()  # scalars returns multiple lines

    return db_meal_plans


def update_meal_plan(
    db: Session, trainer_id: UUID, meal_plan_id: UUID, plan_data: MealPlanUpdate
) -> Optional[MealPlan]:

    db_meal_plan = read_meal_plan(db, trainer_id, meal_plan_id)

    if not db_meal_plan:
        return None

    db_meal_plan.name = plan_data.name

    delete_statement = delete(MealPlanEntry).where(
        MealPlanEntry.meal_plan_id == meal_plan_id
    )
    db.execute(delete_statement)

    for entry_data in plan_data.meal_entries:
        db_entry = MealPlanEntry(
            meal_plan_id=db_meal_plan.id,
            base_meal_id=entry_data.base_meal_id,
            serving_size_grams=entry_data.serving_size_grams,
            time_slot=entry_data.time_slot,
            notes=entry_data.notes,
            carbohydrates_g=entry_data.carbohydrates_g,
            fat_g=entry_data.fat_g,
            protein_g=entry_data.protein_g,
        )
        db.add(db_entry)

    db.commit()
    db.refresh(db_meal_plan)

    return db_meal_plan


def delete_meal_plan(db: Session, trainer_id: UUID, meal_plan_id: UUID) -> bool:

    db_meal_plan = read_meal_plan(db, trainer_id, meal_plan_id)

    if not db_meal_plan:
        return False

    delete_entries_statement = delete(MealPlanEntry).where(
        MealPlanEntry.meal_plan_id == meal_plan_id
    )
    db.execute(delete_entries_statement)

    db.delete(db_meal_plan)
    db.commit()

    return True
