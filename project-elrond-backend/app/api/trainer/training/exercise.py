from fastapi import APIRouter, Header
from app.crud.trainer.training.exercises import get_all_exercise
from app.crud.trainer.training.exercises import get_exercise_by_id


router = APIRouter()

@router.get("/trainer/exercises/", tags=["Trainer"])
def read_all_exercise():
    return get_all_exercise()

@router.get("/trainer/exercises/{exercise_id}", tags=["Trainer"])
def read_exercise(exercise_id: int):
    return get_exercise_by_id(exercise_id)