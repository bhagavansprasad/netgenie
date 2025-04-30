from fastapi import Depends, HTTPException, status, Request, FastAPI
from app.core.security import get_current_user
from app.core.database import get_database
import logging
from app.schemas.user_schemas import UserResponse # Import UserResponse

logger = logging.getLogger(__name__)

from fastapi import Request

async def check_permission(request: Request, user: UserResponse = Depends(get_current_user), db = Depends(get_database)):
    """
    Checks if the user's role has permission to access the requested endpoint.
    Now uses request.scope["route"].name to get the route name.
    """
    logger.debug("Entering check_permission function")
    logger.debug(f"Request URL: {request.url}")
    logger.debug(f"Request Method: {request.method}")

    endpoint_name = request.scope["route"].name  # Get the route name directly from the request

    logger.debug(f"Endpoint name found: {endpoint_name}")

    if not endpoint_name:
        logger.warning(f"No route name found for endpoint path: {request.url.path}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Endpoint not found"
        )

    logger.debug(f"Checking permission for endpoint: {endpoint_name}, method: {request.method}, user: {user}")

    permission = await db["endpoint_permissions"].find_one(
        {"endpoint_name": endpoint_name, "role_id": user.role_id, "method": request.method}  # Changed to user.role_id
    )

    logger.debug(f"Permission record: {permission}")

    if permission:
        logger.info(f"User '{user.username}' authorized to access endpoint: {endpoint_name}") # Changed to user.username
        logger.debug("Exiting check_permission function - Permission Granted")
        return  # Permission granted
    else:
        logger.warning(f"User '{user.username}' does not have permission to access endpoint: {endpoint_name}") # Changed to user.username
        logger.debug("Exiting check_permission function - Permission Denied")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )
