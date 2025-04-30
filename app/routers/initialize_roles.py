from fastapi import APIRouter, Depends
from pymongo import MongoClient
import logging
from app.core.database import get_database
import pymongo  # Import pymongo for error handling

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

async def initialize_roles(db):
    """Inserts roles into the 'roles' collection if it's empty."""
    COLLECTION_NAME = "roles"  # Assuming you are calling from database
    collection = db[COLLECTION_NAME] #get the name of the collection

    # Check if the collection is empty before inserting
    if await collection.count_documents({}) == 0:
        try:
            # Define roles to insert, including both _id and id
            roles = [
                {"_id": 1, "id": 1, "name": "admin", "description": "Administrator"},
                {"_id": 2, "id": 2, "name": "netarch", "description": "Network Architect"},
                {"_id": 3, "id": 3, "name": "neteng", "description": "Network Engineer"},
            ]
            # Insert roles into the collection
            await collection.insert_many(roles)
            logger.info("Roles inserted successfully!")

        except pymongo.errors.BulkWriteError as e:
            # Handle the case where documents with the same _id already exist
            logger.warning(f"BulkWriteError occurred: {e.details}") # log the details
            logger.info("Roles insertion likely failed due to duplicate _id values.  Collection might be partially initialized.")
        except Exception as e:
            logger.error(f"Error inserting roles: {e}")  # Handle potential errors

    else:
        logger.info("Roles collection already initialized. Skipping insertion.")

async def on_startup_db_initialize():
    db = await get_database()
    await initialize_roles(db)
