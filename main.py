from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from dotenv import load_dotenv
import os
import redis.asyncio as aioredis
from routes.users import router as users_router
from routes.roles import router as roles_router
from routes.permissions import router as permissions_router
from schemas import ResponseSchema
from services.helpers import allow_access

load_dotenv()

# Database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    service_uri = os.getenv("REDIS_URL")
    redis = aioredis.from_url(service_uri)
    # Test the connection
    await redis.ping()
    print("Connected to Redis successfully")
    yield
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
