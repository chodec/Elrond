from app.schemas.exercise import ExerciseRead
from app.crud.forms import mock_db_exercise

def get_all_exercise():
    return mock_db_exercise

def get_exercise_by_id(exercise_id: int):
    for exercise in mock_db_exercise:
        if exercise["id"] == exercise_id:
            return exercise
    return "Not found"