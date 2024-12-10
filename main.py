from asyncio import create_task
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from routes.permissions import router as permissions_router
from routes.roles import router as roles_router
from routes.users import router as users_router
from schemas import ResponseSchema
from services.helpers import allow_access
from services.log import move_logs_to_mysql
from services.redis import redis
import os

load_dotenv()

# Database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):   
    # Test the connection
    await redis.ping()
    task = create_task(move_logs_to_mysql())
    print("Connected to Redis successfully")
    yield
    task.cancel()
    await redis.close()


app = FastAPI(lifespan=lifespan)
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(roles_router, prefix="/roles", tags=["Roles"])
app.include_router(permissions_router, prefix="/permissions", tags=["Permissions"])


@app.get("/")
async def root():
    return ResponseSchema(success=True, message="Accessed open endpoint")


@app.get("/billing", dependencies=[Depends(allow_access())])
def billing():
    return ResponseSchema(
        success=True,
        message="Accessed the billing API which is only accessible by Admins",
    )


@app.get("/metrics", dependencies=[Depends(allow_access(["Supervisor"]))])
def metrics():
    return ResponseSchema(
        success=True,
        message="Accessed the metrics API which is only accessible by Supervisors and Admins",
    )


@app.get("/all", dependencies=[Depends(allow_access(["*"]))])
def all():
    return ResponseSchema(
        success=True,
        message="Accessed the all API which is accessible by all valid users",
    )
