import os
import redis.asyncio as aioredis
from dotenv import load_dotenv

load_dotenv()

service_uri = os.getenv("REDIS_URL")
redis = aioredis.from_url(service_uri)