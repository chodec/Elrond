from app.schemas.meal_plan import MealPlanRead
from app.crud.forms import mock_db_meal_plan

def get_all_meal_plans():
    return mock_db_meal_plan

def get_meal_plan_by_id(meal_plan_id: int):
    for plan in mock_db_meal_plan:
        if plan["id"] == meal_plan_id:
            return plan
    return "Not found"
