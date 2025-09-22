from fastapi import APIRouter, Header
from app.crud.trainer.meals import get_all_meals
from app.crud.trainer.meals import get_meal_by_id
from app.crud.trainer.meals import create_meal

router = APIRouter()

@router.get("/trainer/meals/", tags=["Trainer"])
def read_all_meal():
    return get_all_meals()

@router.get("/trainer/meals/{meal_id}", tags=["Trainer"])
def read_meal(meal_id: int):
    return get_meal_by_id(meal_id)

@router.post("/trainer/meals/", tags=["Trainer"])
def create_meal_plan(meal_name: str =  Header(...)):
    return create_meal(meal_name)

@router.delete("/trainer/meals/{meal_id}", tags=["Trainer"])
def delete_meal_plan(meal_id: int):
    return {"message": f"Delete {meal_id}"}