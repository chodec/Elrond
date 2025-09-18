from fastapi import APIRouter
from .trainer import meal_plan
from .trainer import meal
from .system import health_check
from .auth import user_type



api_router = APIRouter()

#trainer
api_router.include_router(meal_plan.router)
api_router.include_router(meal.router)
#system
api_router.include_router(health_check.router)
#auth
api_router.include_router(user_type.router)