from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.file import router
from contextlib import asynccontextmanager
from app.redis.client import init_redis
from app.config import config
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager to initialize and clean up resources.
    """
    # Create the upload folder if it does not exist
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    print(f"Upload folder created at: {config.UPLOAD_FOLDER}")
    # Initialize Redis client
    redis_client = init_redis()
    if redis_client is None:
        raise RuntimeError("Failed to connect to Redis")
    
    try:
        yield  # Yield control back to the application
    finally:
        # Clean up resources if necessary
        pass

app= FastAPI(lifespan=lifespan)
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the file router
app.include_router(router, prefix="/api", tags=["file"])