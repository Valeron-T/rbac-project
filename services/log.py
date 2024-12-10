from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio
import json
from services.redis import redis
from models import AccessLog
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("ASYNC_DB_URL")

# Create an async engine
async_engine = create_async_engine(DATABASE_URL, future=True)

# Create an async session
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def move_logs_to_mysql():
    """
    Background task to move logs from Redis to MySQL.
    """
    while True:
        logs = []
        async with AsyncSessionLocal() as db:  # Async session for database
            while True:
                # Pop a log entry from Redis
                log_entry = await redis.rpop("access_logs")
                if not log_entry:
                    break
                logs.append(json.loads(log_entry))

            if logs:
                # Batch write logs to MySQL
                db.add_all([AccessLog(**log) for log in logs])
                await db.commit()  # Async commit

        # Wait before fetching more logs
        await asyncio.sleep(10)
