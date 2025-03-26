from fastapi import APIRouter, Body, HTTPException, Query
from app.ai import ai_interface
from app.models.config_model import ConfigModel
from typing import Dict, List
import logging
from app.core.database import get_database

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)

@router.get("/customers")
async def list_customers():
    db = get_database()
    customers = list(db["customers"].find())  # Get all customers as a list
    # Convert ObjectId to string for JSON serialization
    for customer in customers:
        customer["_id"] = str(customer["_id"])
    return customers