from fastapi import APIRouter
from .trainer.meal import meal_plan
from .trainer.meal import meal
from .trainer.training import exercise
from .trainer.training import exercise_plan
from .trainer.subscription import subscription
from .trainer.requests import client_trainer_requests
from .client import measurement
from .client import subscription as client_subscriptions
from .client import client_trainer_requests as client_requests
from .system import health_check
from .auth import register

api_router = APIRouter()

#trainer operations 
api_router.include_router(
    meal_plan.router,
    prefix = "/trainer"
    )

api_router.include_router(
    meal.router,
    prefix = "/trainer"
    )

api_router.include_router(
    exercise.router,
    prefix = "/trainer"
    )

api_router.include_router(
    exercise_plan.router,
    prefix = "/trainer"
    )

api_router.include_router(
    subscription.router,
    prefix = "/trainer"
    )
api_router.include_router(
    client_trainer_requests.router, 
    prefix = "/trainer"
)

#client operations
api_router.include_router(
    measurement.router,
    prefix = "/client"
    )

api_router.include_router(
    client_requests.router,
    prefix = "/client"
)

api_router.include_router(
    client_subscriptions.router,
    prefix = "/client"
)


#system
api_router.include_router(
    health_check.router,
    prefix = "/system"
    )

#auth
api_router.include_router(
    register.router, 
    prefix = "/auth"
)