from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.db.models import ExercisePlan as dbExercisePlan, ExercisePlanEntry as dbExercisePlanEntry
from app.schemas.exercise_plan import ExercisePlanEntryCreate 


def create_exercise_plan(
        db: Session,
        plan_name: str,
        trainer_id: UUID,
        notes: str | None,
        exercise_entries_data: List[ExercisePlanEntryCreate]
) -> dbExercisePlan:
    
    db_exercise_plan = dbExercisePlan(
        name=plan_name,
        trainer_id=trainer_id,
        notes=notes
    )
    
    db.add(db_exercise_plan)
    # Flush for get id before query
    db.flush() 
    
    for entry_data in exercise_entries_data:
        db_entry = dbExercisePlanEntry(
            exercise_plan_id=db_exercise_plan.id,
            
            base_exercise_id=entry_data.base_exercise_id,
            sets=entry_data.sets,
            repetitions=entry_data.repetitions,
            
            day_of_week=entry_data.day_of_week, 
            
            order_in_session=entry_data.order_in_session, 
            notes=entry_data.notes
        )
        db.add(db_entry)
        
    db.commit()
    db.refresh(db_exercise_plan)
    
    return db_exercise_plan
