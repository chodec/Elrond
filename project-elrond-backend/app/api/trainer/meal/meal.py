from fastapi import APIRouter, Header
from app.crud.trainer.meal.meals import get_all_meals
from app.crud.trainer.meal.meals import get_meal_by_id
from app.crud.trainer.meal.meals import create_new_meal
from app.crud.trainer.meal.meals import delete_meal_by_id

router = APIRouter()

@router.get("/trainer/meals/", tags=["Trainer"])
def read_all_meal():
    return get_all_meals()

@router.get("/trainer/meals/{meal_id}", tags=["Trainer"])
def read_meal(meal_id: int):
    return get_meal_by_id(meal_id)

@router.post("/trainer/meals/", tags=["Trainer"])
def create_meal(meal_name: str =  Header(...)):
    return create_new_meal(meal_name)

@router.delete("/trainer/meals/", tags=["Trainer"])
def delete_meal(meal_id: int =  Header(...)):
    return ddelete_meal_by_id(meal_id)