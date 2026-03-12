from fastapi import FastAPI
from app import routers, models, database
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()

# Create DB tables
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

app.include_router(routers.router)

@app.get("/")
def root():
    return {"message": "Welcome to Voice2Invoice API"}
