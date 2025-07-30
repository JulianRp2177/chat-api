from tortoise import Tortoise
from fastapi import FastAPI
from app.core.config import settings

async def init_db(app: FastAPI) -> None:
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.message"]},
    )
    await Tortoise.generate_schemas() 
