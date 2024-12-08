from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

# Database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
