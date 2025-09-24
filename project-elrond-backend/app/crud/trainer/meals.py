from app.schemas.meal_plan import MealPlanRead
from app.crud.forms import mock_db_meal


def get_all_meals():
    return mock_db_meal

def get_meal_by_id(meal_id: int):
    for meal in mock_db_meal:
        if meal["id"] == meal_id:
            return meal
    return "Not found"

def create_new_meal(meal_name: str):
    last_item = mock_db_meal[-1]
    new_id = last_item["id"] + 1
    return {new_id: meal_name}

def delete_meal_by_id(meal_id: int):
    for meal in mock_db_meal:
        if meal["id"] == meal_id:
            mock_db_meal.remove(meal)
            return "{meal} removed"
    return "Not found"