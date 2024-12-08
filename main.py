from fastapi import FastAPI
from dotenv import load_dotenv
import os

from routes.users import router as users_router
from routes.roles import router as roles_router
from routes.permissions import router as permissions_router

load_dotenv()

# Database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

app = FastAPI()
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(roles_router, prefix="/roles", tags=["Roles"])
app.include_router(permissions_router, prefix="/permissions", tags=["Permissions"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
