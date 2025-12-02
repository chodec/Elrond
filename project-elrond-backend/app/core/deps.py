from typing import Optional
from fastapi import Header
from app.schemas.user import UserRead
from app.schemas.user import UserRead, UserRole


def get_current_user(x_user_type: Optional[str] = Header(None)):
    if x_user_type == "admin":
        mock_user = UserRead(
            id=1,
            email="trainer@example.com",
            first_name="John",
            last_name="Hoe",
            role=UserRole.TRAINER,
        )
    elif x_user_type == "client":
        mock_user = UserRead(
            id=2,
            email="client@example.com",
            first_name="Mitch",
            last_name="Oken",
            role=UserRole.CLIENT,
        )
    else:
        mock_user = UserRead(
            id=3,
            email="pending@example.com",
            first_name="Gabe",
            last_name="Itch",
            role=UserRole.PENDING,
        )

    return mock_user
