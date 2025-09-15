from fastapi import APIRouter
from .trainer import meal_plan
from .system import health_check
from .auth import user_type

api_router = APIRouter()

api_router.include_router(meal_plan.router)
api_router.include_router(health_check.router)
api_router.include_router(user_type.router)