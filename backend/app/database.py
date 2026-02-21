"""Database connections for MongoDB and PostgreSQL."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from app.config import settings

# PostgreSQL setup
engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB setup
mongodb_client: AsyncIOMotorClient = None
mongodb_sync_client: MongoClient = None


def get_db():
    """Get PostgreSQL database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_mongodb():
    """Get MongoDB database instance."""
    return mongodb_client[settings.mongodb_db_name]


def get_mongodb_sync():
    """Get synchronous MongoDB client."""
    return mongodb_sync_client[settings.mongodb_db_name]


async def connect_mongodb():
    """Connect to MongoDB."""
    global mongodb_client, mongodb_sync_client
    mongodb_client = AsyncIOMotorClient(settings.mongodb_uri)
    mongodb_sync_client = MongoClient(settings.mongodb_uri)


async def disconnect_mongodb():
    """Disconnect from MongoDB."""
    global mongodb_client, mongodb_sync_client
    if mongodb_client:
        mongodb_client.close()
    if mongodb_sync_client:
        mongodb_sync_client.close()
