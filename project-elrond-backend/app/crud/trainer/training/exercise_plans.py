from app.schemas.exercise_plan import ExercisePlanRead
from app.crud.forms import mock_db_exercise_plan

def get_all_exercise_plan():
    return mock_db_exercise_plan

def get_exercise_plan_by_id(exercise_plan_id: int):
    for exercise_plan in mock_db_exercise_plan:
        if exercise_plan["id"] == exercise_plan_id:
            return exercise_plan
    return "Not found"