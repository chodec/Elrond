from pydantic import BaseModel
import uuid 
from uuid import UUID 

class TrainerFinalize(BaseModel): 
    user_id: UUID
    specialization: str | None = None