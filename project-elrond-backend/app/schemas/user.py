from enum import Enum
from pydantic import BaseModel

class UserRole(str, Enum):
    CLIENT = "client"
    TRAINER = "trainer"
    PENDING = "pending"

class UserRead(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: UserRole
    