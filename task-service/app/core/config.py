from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dotenv import load_dotenv
import os


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_async_engine(DATABASE_URL, echo=True, future=True)
sync_database_url = DATABASE_URL.replace("asyncpg", "psycopg2")
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        yield db


def create_tables():
    Base.metadata.create_all(bind=sync_engine)
