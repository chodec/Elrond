from fastapi import APIRouter
from app.crud.trainer.meal_plans import get_all_meal_plans
from app.crud.trainer.meal_plans import get_meal_plan_by_id

router = APIRouter()

@router.get("/trainer/meal-plans/", tags=["Trainer"])
def read_all_meal_plans():
    return get_all_meal_plans()

@router.get("/trainer/meal-plans/{meal_plan_id}", tags=["Trainer"])
def read_meal_plan(meal_plan_id: int):
    return get_meal_plan_by_id(meal_plan_id)

@router.post("/trainer/meal-plans/", tags=["Trainer"])
def create_meal_plan():
    return {"message": "Create a meal plan"}

@router.delete("/trainer/meal-plans/{meal_plan_id}", tags=["Trainer"])
def delete_meal_plan(meal_plan_id: int):
    return {"message": f"Delete {meal_plan_id}"}