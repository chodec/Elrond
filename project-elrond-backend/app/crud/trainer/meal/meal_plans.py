from app.schemas.meal_plan import MealPlanRead
from app.crud.forms import mock_db_meal_plan

def get_all_meal_plans():
    return mock_db_meal_plan

def get_meal_plan_by_id(meal_plan_id: int):
    for meal_plan in mock_db_meal_plan:
        if meal_plan["id"] == meal_plan_id:
            return meal_plan
    return "Not found"

def create_new_meal_plan(meal_plan_name: str, meals_id: list):
    last_item = mock_db_meal_plan[-1]
    new_id = last_item["id"] + 1
    new_meal_plan = {
        "id": new_id,
        "name": meal_plan_name,
        "trainer_id": 1,
        "meals": meals_id
    }
    return new_meal_plan

def delete_meal_plan(meal_plan_id: int):
    for meal_plan in mock_db_meal_plan:
        if meal_plan["id"] == meal_plan_id:
            mock_db_meal.remove(meal_plan)
            return "{meal_plan} removed"
    return "Not found"
