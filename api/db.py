import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE = "mysql+aiomysql"
USER = os.getenv("DB_USER", "inventory_user")
PASSWORD = os.getenv("DB_PASSWORD", "inventory_password")
HOST = os.getenv("DB_HOST", "mysql")
PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "inventory")

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "{}://{}:{}@{}:{}/{}".format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
)

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
