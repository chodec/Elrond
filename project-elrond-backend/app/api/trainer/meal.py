from fastapi import APIRouter
from app.crud.trainer.meals import get_all_meals
from app.crud.trainer.meals import get_meal_by_id

router = APIRouter()

@router.get("/trainer/meals/", tags=["Trainer"])
def read_all_meal():
    return get_all_meals()

@router.get("/trainer/meals/{meal_id}", tags=["Trainer"])
def read_meal(meal_id: int):
    return get_meal_by_id(meal_id)

@router.post("/trainer/meal/", tags=["Trainer"])
def create_meal_plan():
    return {"message": "Create a meal plan"}

@router.delete("/trainer/meal/{meal_id}", tags=["Trainer"])
def delete_meal_plan(meal_id: int):
    return {"message": f"Delete {meal_id}"}