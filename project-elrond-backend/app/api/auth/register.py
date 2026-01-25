from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.db.models import Role
from app.schemas.user import (
    UserInitialCreate,
    UserUpdate,
    RoleUpgrade,
    User as UserSchema,
)
from app.crud.auth.user import (
    create_pending_user,
    get_user_by_email,
    upgrade_user_profile,
    update_user_data,
    get_user_by_id,
)

router = APIRouter(tags=["Auth"])

@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    description="Create a pending user account.",
)
def register_user(data: UserInitialCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, email=data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email already exists"
        )
    
    try:
        return create_pending_user(db, user_data=data)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/onboard",
    status_code=status.HTTP_200_OK,
    description="User specifies if they are a client or trainer.",
)
def onboard_user_profile(role_choice: RoleUpgrade, db: Session = Depends(get_db)):
    # Validace role přímo v endpointu je správná
    if role_choice.role not in [Role.CLIENT, Role.TRAINER]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid role selection. Choose CLIENT or TRAINER."
        )

    try:
        upgrade_user_profile(
            db, user_id=role_choice.user_id, new_role=role_choice.role
        )
        return {
            "message": "Role upgraded successfully.",
            "new_role": role_choice.role.value,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/user/{user_id}",
    response_model=UserSchema,
    description="Get specific user data by ID.",
)
def read_user_data(user_id: UUID, db: Session = Depends(get_db)):
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
    description="Update user's name or password.",
)
def update_user_data_by_id(
    user_id: UUID, data: UserUpdate, db: Session = Depends(get_db)
):
    if data.name is None and data.password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update."
        )

    try:
        return update_user_data(db, user_id=user_id, user_data=data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))