from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud.system.health_check import check_db_health

router = APIRouter(tags=["System"])

@router.get(
    "/health/api", 
    description="Liveness probe: Checks if the FastAPI application is running."
)
def get_api_health():
    return {"status": "online", "timestamp": "ok"}

@router.get(
    "/health/db", 
    description="Readiness probe: Checks if the database is reachable."
)
def get_db_health(db: Session = Depends(get_db)):
    """
    Checks the database connectivity by executing a simple 'SELECT 1'.
    Returns 200 if OK, 503 if the database is unavailable.
    """
    is_healthy = check_db_health(db)
    
    if is_healthy:
        return {
            "status": "ready",
            "database": "connected",
            "mode": "synchronous"
        }
    
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
        detail="Database connection failed or database is down"
    )