from enum import Enum
import uuid 
from uuid import UUID 
from pydantic import EmailStr
from pydantic import BaseModel

class UserRole(str, Enum):
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
    