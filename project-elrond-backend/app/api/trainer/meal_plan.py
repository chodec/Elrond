from fastapi import APIRouter

router = APIRouter()

@router.get("/trainer/meal-plans/", tags=["Trainer"])
def read_all_meal_plans():
    return {"message": "Get all meal plans"}

@router.get("/trainer/meal-plans/{meal_plan_id}", tags=["Trainer"])
def read_all_meal_plans():
    return {"message": "Get {meal_plan_id}"}

@router.post("/trainer/meal-plans/", tags=["Trainer"])
def create_meal_plan():
    return {"message": "Create a meal plan"}

@router.delete("/trainer/meal-plans/{meal_plan_id}", tags=["Trainer"])
def create_meal_plan():
    return {"message": "Delete {meal_plan_id}"}