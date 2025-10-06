from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID 
from app.db.database import get_db 
from app.db.models import User, Role 
from app.schemas.user import UserInitialCreate,RoleUpgrade, User as UserSchema 
from app.crud.auth.user import create_pending_user, get_user_by_email, upgrade_user_profile

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

    db_user = get_user_by_email(db, email=data.email)

    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    new_user = create_pending_user(db, user_data=data)
    
    # validate jwt later
    
    return new_user

@router.post("/onboard", status_code=status.HTTP_200_OK)
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
