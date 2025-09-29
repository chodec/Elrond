from fastapi import APIRouter, Header
from app.crud.trainer.meal.meal_plans import get_all_meal_plans
from app.crud.trainer.meal.meal_plans import get_meal_plan_by_id
from app.crud.trainer.meal.meal_plans import create_new_meal_plan

router = APIRouter()

@router.get("/trainer/meal-plans/", tags=["Trainer"])
def read_all_meal_plans():
    return get_all_meal_plans()

@router.get("/trainer/meal-plans/{meal_plan_id}", tags=["Trainer"])
def read_meal_plans(meal_plan_id: int):
    return get_meal_plan_by_id(meal_plan_id)

@router.post("/trainer/meal-plans/", tags=["Trainer"])
def create_meal_plan(meal_plan_name: str = Header(...), meals_id: str = Header(...)):
    list_of_ids = [int(i) for i in meals_id.split(',')]
    return create_new_meal_plan(meal_plan_name,list_of_ids)

@router.delete("/trainer/meal-plans", tags=["Trainer"])
def delete_meal_plan(meal_plan_id: int = Header(...)):
    return {"message": f"Delete {meal_plan_id}"}