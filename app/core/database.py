import motor.motor_asyncio
from app.core.settings import settings
import logging

logger = logging.getLogger(__name__)

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
database = client[settings.MONGODB_DB_NAME]

async def get_database():
    """Returns the MongoDB database object."""
    logger.info(f"Getting the database connection to db {settings.MONGODB_DB_NAME}")
    return database