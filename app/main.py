from fastapi import FastAPI, Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import logging
from app.routers import ifaceconfig
from app import logging_config
from app.routers import initialize_roles
from app.routers import initialize_users
from app.routers import auth_router
from app.routers import user_router
from app.routers import role_router
from app.core.database import get_database
from contextlib import asynccontextmanager
from app.core.security import custom_openapi
from app.core.security import get_current_user
logging_config.configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(dependencies=[Depends(get_current_user)]) #Add the dependencies to every endpoints
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI to manage startup and shutdown tasks.
    """
    logger.info("Starting up...")
    db = await get_database()
    await initialize_roles.on_startup_db_initialize()
    await initialize_users.on_startup_db_initialize_users()
    logger.info("Startup tasks completed.")
    yield
    logger.info("Shutting down...")
    
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router, prefix="", tags=["Authentication"])
app.include_router(user_router.router, prefix="", tags=["Users"])
app.include_router(role_router.router, prefix="", tags=["Roles"])
app.include_router(ifaceconfig.router, prefix="", tags=["Config"])

app.openapi = lambda: custom_openapi(app)

