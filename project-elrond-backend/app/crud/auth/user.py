from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, SQLAlchemyError
from typing import Optional
from uuid import UUID
from app.db.models import User, Role, Client, Trainer
from app.schemas.user import UserInitialCreate, UserUpdate


def get_password_hash(password: str) -> str:
    return f"hashed_{password}_placeholder"  # hash later


from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def create_pending_user(db: Session, user_data: UserInitialCreate) -> User:
    try:
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                name=user_data.name,
                role=Role.PENDING,
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Email is already used.")
    except OperationalError:
        db.rollback()
        raise HTTPException(503, "Database is currently not working.")
    except DataError:
        db.rollback()
        raise HTTPException(400, "Incorect data format.")
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}") 
        raise HTTPException(500, "Something is completly wrong.")

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    return db.get(User, user_id)

def upgrade_user_profile(
    db: Session, user_id: UUID, new_role: Role, specialization: str | None = None
) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise ValueError("User not found")

    if db_user.role != Role.PENDING:
        raise ValueError(f"User already has role: {db_user.role.value}")

    try:
        if new_role == Role.CLIENT:
            db_user.role = Role.CLIENT
            db_client = Client(user_id=user_id)
            db.add(db_client)

        elif new_role == Role.TRAINER:
            db_user.role = Role.TRAINER
            db_trainer = Trainer(user_id=user_id, specialization=specialization)
            db.add(db_trainer)
        else:
            raise ValueError("Invalid role upgrade target")

        db.commit()
        db.refresh(db_user)
        return db_user

    except (IntegrityError, SQLAlchemyError) as e:
        db.rollback()
        raise RuntimeError(f"Database error during profile upgrade: {str(e)}")

def update_user_data(db: Session, user_id: UUID, user_data: UserUpdate) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise ValueError("User not found")

    try:
        if user_data.name is not None:
            db_user.name = user_data.name

        if user_data.password is not None:
            db_user.hashed_password = get_password_hash(user_data.password)

        db.commit()
        db.refresh(db_user)
        return db_user

    except (IntegrityError, SQLAlchemyError) as e:
        db.rollback()
        raise RuntimeError(f"Database error during user update: {str(e)}")