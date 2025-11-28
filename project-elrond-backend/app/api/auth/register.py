from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import os
from dotenv import load_dotenv
from app.db.database import get_db 
from app.db.models import Role 
from app.schemas.user import UserInitialCreate, UserUpdate, RoleUpgrade, User as UserSchema 
from app.crud.auth.user import (
    create_pending_user,
    get_user_by_email,
    upgrade_user_profile,
    update_user_data,
    get_user_by_id
)

router = APIRouter(tags=["Auth"])

@router.post(
    "/register", 
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    description="Create account"
)
def register_user(
    data: UserInitialCreate, 
    db: Session = Depends(get_db)
):

    db_user = get_user_by_email(db, email=data.email)

    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    new_user = create_pending_user(db, user_data=data)
    
    # validate jwt later
    
    return new_user

@router.post(
        "/onboard",
        status_code=status.HTTP_200_OK,
        description="User specify if he is client or trainer"
)
def onboard_user_profile(
    role_choice: RoleUpgrade,
    db: Session = Depends(get_db)
):

    target_role_value = role_choice.role.value

    if target_role_value not in [Role.CLIENT.value, Role.TRAINER.value]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Not valid role."
        )

    try:
        upgrade_user_profile(
            db, 
            user_id=role_choice.user_id,
            new_role=Role(target_role_value)
        )
        
    except ValueError as e:
        status_code_to_return = status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=status_code_to_return, 
            detail=f"Upgrade failed: {str(e)}"
        )
        
    return {
        "message": f"New role set: {target_role_value}.",
        "new_role": target_role_value
    }

@router.get(
    "/user/{user_id}", 
    response_model=UserSchema,
    description="Get specific user data by ID (for viewing/editing)."
)
def read_user_data(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_id(db, user_id=user_id)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found."
        )
        
    return db_user

@router.put(
    "/user/{user_id}",
    response_model=UserSchema,
    description="Update user's name or password by ID."
)
def update_user_data_by_id(
    user_id: UUID,
    data: UserUpdate, 
    db: Session = Depends(get_db)
):
    if data.name is None and data.password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="At least one field (name or password) must be provided for update."
        )

    try:
        updated_user = update_user_data(
            db, 
            user_id=user_id,
            user_data=data
        )
        
    except ValueError as e:
        
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=status_code, 
            detail=f"Update failed: {str(e)}"
        )
        
    return updated_user