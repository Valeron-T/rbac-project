from asyncio import create_task
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes.permissions import router as permissions_router
from routes.roles import router as roles_router
from routes.users import router as users_router
from routes.logging import router as logs_router
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
app.include_router(logs_router, prefix="/logs", tags=["Logs"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for request validation errors.
    """
    errors = []
    for error in exc.errors():
        loc = " -> ".join(map(str, error.get("loc", [])))
        msg = error.get("msg", "Validation error")
        ctx = error.get("ctx", {})
        if ctx and "expected" in ctx:
            msg += f" (Expected: {ctx['expected']})"
        errors.append({"field": loc, "message": msg})

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": errors,
        },
    )


@app.get("/")
async def root():
    return ResponseSchema(success=True, message="Accessed open endpoint")


@app.get("/billing", dependencies=[Depends(allow_access())])
def billing():
    """API only accessible by admins"""
    return ResponseSchema(
        success=True,
        message="Accessed the billing API which is only accessible by Admins",
    )


@app.get("/metrics", dependencies=[Depends(allow_access(["Supervisor"]))])
def metrics():
    """API only accessible by supervisors and admins"""
    return ResponseSchema(
        success=True,
        message="Accessed the metrics API which is only accessible by Supervisors and Admins",
    )


@app.get("/all", dependencies=[Depends(allow_access(["*"]))])
def all():
    """API accessible by valid users"""
    return ResponseSchema(
        success=True,
        message="Accessed the all API which is accessible by all valid users",
    )
