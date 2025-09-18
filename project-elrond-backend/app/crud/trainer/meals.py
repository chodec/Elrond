from app.schemas.meal_plan import MealPlanRead
from app.crud.forms import mock_db_meal


def get_all_meals():
    return mock_db_meal

def get_meal_by_id(meal_id: int):
    for meal in mock_db_meal:
        if meal["id"] == meal_id:
            return meal
    return "Not found"
