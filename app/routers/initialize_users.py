from fastapi import APIRouter, Depends
import logging
from app.core.database import get_database
from app.schemas.user_schemas import UserCreate

router = APIRouter()

logger = logging.getLogger(__name__)

async def initialize_users(db):
    """Inserts initial user accounts into the 'users' collection if it's empty (PLAIN TEXT PASSWORDS - INSECURE!)."""
    collection = db["users"]  # Get the users collection

    if await collection.count_documents({}) == 0:
        try:
            # Define the initial users (using UserCreate)
            initial_users = [
                UserCreate(username="bhagavan", password="jnjnuh", role_id=1, email="bhagavan@example.com"),
            ]

            # Prepare data for insertion (NO PASSWORD HASHING - INSECURE!)
            users_to_insert = []
            for user in initial_users:
                user_data = {
                    "id": await get_next_sequence(db, "user_id"), # get id using the sequence
                    "username": user.username,
                    "password": user.password,  # STORED IN PLAIN TEXT - **VERY INSECURE!**
                    "role_id": user.role_id,
                    "email": user.email,
                }
                users_to_insert.append(user_data)

            # Insert the users into the collection
            await collection.insert_many(users_to_insert)
            logger.info("Initial users inserted successfully (PLAIN TEXT PASSWORDS!).")

        except Exception as e:
            logger.exception(f"Error inserting initial users: {e}")  # Log the full exception
    else:
        logger.info("Users collection already initialized. Skipping user insertion.")

#Helper to get the next id
async def get_next_sequence(db, sequence_name: str):
    """Atomically increments the sequence number in the 'counters' collection."""
    result = await db["counters"].find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True,  # Return the updated document
    )
    if result:
        return result["seq"]
    else:
        # Initialize sequence if it doesn't exist
        await db["counters"].insert_one({"_id": sequence_name, "seq": 1})
        return 1

# Call this function during app startup (See main.py)
async def on_startup_db_initialize_users():
    logger.info("Entering on_startup_db_initialize_users function")
    db = await get_database()
    await initialize_users(db)
