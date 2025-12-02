from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud.system.health_check import check_db_health

router = APIRouter()


@router.get("/health_check_api", tags=["System"], description="Check if API is active")
def get_api_health():
    return {"status": "200"}


@router.get("/health_check_db", tags=["System"], description="Check if DB is active")
def get_db_health(db: Session = Depends(get_db)):
    if check_db_health(db):
        return {"status": "ok", "database": "up", "type": "synchronous"}
    else:
        raise HTTPException(
            status_code=503, detail="Database connection failed or database is down"
        )
