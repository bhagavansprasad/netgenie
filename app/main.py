from fastapi import FastAPI
from app.routers import ifaceconfig, user, network
from app import logging_config  # Import the logging configuration

app = FastAPI()

# Configure logging
logging_config.configure_logging()

app.include_router(ifaceconfig.router)
# app.include_router(user.router)
# app.include_router(network.router)
