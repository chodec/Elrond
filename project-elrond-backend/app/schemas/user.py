from enum import Enum as PyEnum
import uuid
from uuid import UUID
from pydantic import EmailStr
from pydantic import BaseModel


class UserRole(str, PyEnum):
    CLIENT = "client"
    TRAINER = "trainer"
    PENDING = "pending"


# Mock data model
class UserRead(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: UserRole


class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None


class UserInitialCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class User(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: UserRole

    class Config:
        from_attributes = True


class RoleUpgrade(BaseModel):
    user_id: UUID
    role: UserRole
