from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID 
from app.db.database import get_db 
from app.schemas.user import UserInitialCreate, User as UserSchema 
from app.crud.auth.user import create_pending_user

router = APIRouter(tags=["Auth"])

@router.post(
    "/register", 
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    data: UserInitialCreate, 
    db: Session = Depends(get_db)
):

    new_user = create_pending_user(db, user_data=data)
    
    # validate jwt later
    
    return new_user