from fastapi import FastAPI
from app.api.system import health_check
from app.api.auth import user_type

app = FastAPI()

app.include_router(health_check.router)
app.include_router(user_type.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
