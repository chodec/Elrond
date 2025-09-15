from typing import Union
from fastapi import APIRouter

router = APIRouter()

@router.get("/system/health_check", tags=["System"])
def read_root():
    return {"status": "200"}