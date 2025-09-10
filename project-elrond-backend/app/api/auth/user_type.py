from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.schemas.user import UserRead

router = APIRouter()

@router.get("/auth/user/type", response_model=UserRead)
def read_current_user(current_user: UserRead = Depends(get_current_user)):
    return current_user