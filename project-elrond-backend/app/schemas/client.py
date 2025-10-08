from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ClientUpdate(BaseModel):
    #tbd
    pass

class Client(BaseModel):
    user_id: UUID
    
    class Config:
        from_attributes = True