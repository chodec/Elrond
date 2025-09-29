from fastapi import APIRouter
from app.crud.trainer.training.exercise_plans import get_all_exercise_plan
from app.crud.trainer.training.exercise_plans import get_exercise_plan_by_id

router = APIRouter()

@router.get("/trainer/exercise_plans/", tags=["Trainer"])
def read_all_meal_plans():
    return get_all_exercise_plan()

@router.get("/trainer/exercise_plans/{exercise_plan_id}", tags=["Trainer"])
def read_exercise(exercise_plan_id: int):
    return get_exercise_plan_by_id(exercise_plan_id)