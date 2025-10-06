from fastapi import APIRouter
from .trainer.meal import meal_plan
from .trainer.meal import meal
from .trainer.training import exercise
from .trainer.training import exercise_plan
from .system import health_check
from .auth import register




api_router = APIRouter()

#trainer``
api_router.include_router(meal_plan.router)
api_router.include_router(meal.router)
api_router.include_router(exercise.router)
api_router.include_router(exercise_plan.router)
#system
api_router.include_router(health_check.router)
#auth
api_router.include_router(
    register.router, 
    prefix="/auth"
)