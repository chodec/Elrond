from sqlalchemy.orm import Session
from app.db.models import User, Role 
from app.schemas.user import UserInitialCreate 

def get_password_hash(password: str) -> str:
    return f"hashed_{password}_placeholder" # hash later

def create_pending_user(db: Session, user_data: UserInitialCreate) -> User:

    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        email=user_data.email, 
        hashed_password=hashed_password, 
        name=user_data.name,
        role=Role.PENDING
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user