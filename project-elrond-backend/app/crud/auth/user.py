from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models import User, Role, Client, Trainer
from app.schemas.user import UserInitialCreate, UserUpdate

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

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def upgrade_user_profile(
    db: Session, 
    user_id: UUID, 
    new_role: Role, 
    specialization: str | None = None
) -> User:
    
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise ValueError("User not found") 

    if db_user.role != Role.PENDING:
        raise ValueError(f"User already got role({db_user.role.value}).")
    
    if new_role == Role.CLIENT:
        db_user.role = Role.CLIENT
        db_client = Client(user_id=user_id) 
        db.add(db_client)
        
    elif new_role == Role.TRAINER:
        db_user.role = Role.TRAINER
        db_trainer = Trainer(user_id=user_id, specialization=None) 
        db.add(db_trainer)
        
    else:
        raise ValueError("Can upgrade only to trainer or client")
    
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

def update_user_data(
    db: Session, 
    user_id: UUID, 
    user_data: UserUpdate 
) -> User:
    
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise ValueError("User not found") 

    if user_data.name is not None:
        db_user.name = user_data.name
        
    if user_data.password is not None:
        db_user.hashed_password = get_password_hash(user_data.password) 
        
    db.commit() 
    db.refresh(db_user) 
    
    return db_user