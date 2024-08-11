# user_management_service/app/main.py

from fastapi import FastAPI
from app.routes import profile_routes
from app.database import engine, Base

# Create the database tables
app = FastAPI()

app.include_router(profile_routes.router)

Base.metadata.create_all(bind=engine)