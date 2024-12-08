from fastapi import FastAPI
from dotenv import load_dotenv
import os

from routes.users import router as users_router

load_dotenv()

# Database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

app = FastAPI()
app.include_router(users_router, prefix="/users", tags=["Users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
