from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routers import config_router
from app import logging_config
from app.routers import initialize_roles
from app.routers import initialize_permissions
from app.routers import initialize_users
from app.routers import auth_router
from app.routers import user_router
from app.routers import role_router
from app.routers import template_router
from app.routers import customers_router
from app.routers import devices_router
from app.routers import config_values_router
from app.core.database import get_database
from contextlib import asynccontextmanager
from app.core.security import custom_openapi
from app.core.security import get_current_user

logging_config.configure_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    db = await get_database()
    await initialize_permissions.on_startup_db_initialize_permissions()
    await initialize_roles.on_startup_db_initialize()
    await initialize_users.on_startup_db_initialize_users()
    logger.info("Startup tasks completed.")
    yield
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend
    # allow_origins=["http://localhost:5173"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers
app.include_router(auth_router.router, prefix="", tags=["Authentication"])
app.include_router(customers_router.router, prefix="", tags=["Customers"])
app.include_router(devices_router.router, prefix="", tags=["Devices"])
app.include_router(template_router.router, prefix="", tags=["Templates"])
app.include_router(config_values_router.router, prefix="", tags=["Config Values"])
app.include_router(config_router.router, prefix="", tags=["Generate Configuration"])
app.include_router(user_router.router, prefix="", tags=["Users"])
app.include_router(role_router.router, prefix="", tags=["Roles"])

app.openapi = lambda: custom_openapi(app)

