from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.file import router
from contextlib import asynccontextmanager
from app.redis.client import init_redis
from app.config import config
import os, threading
from app.services.consumerService import consumer_service, stop_event
from app.services.threadService import executor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager to initialize and clean up resources.
    """
    # Create the upload folder if it does not exist
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    print(
        f"Upload and result folder created at {config.UPLOAD_FOLDER} and {config.RESULTS_DIR} folder "
    )

    redis_client = init_redis()
    if redis_client is None:
        raise RuntimeError("Failed to connect to Redis")

    consumer_thread = threading.Thread(target=consumer_service, daemon=True)
    consumer_thread.start()
    app.state.consumer_thread = consumer_thread

    try:
        yield
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        stop_event.set()
        if (
            hasattr(app.state, "consumer_thread")
            and app.state.consumer_thread.is_alive()
        ):
            app.state.consumer_thread.join(timeout=5)
            if app.state.consumer_thread.is_alive():
                print("Warning: Consumer thread did not stop gracefully.")
        executor.shutdown(wait=True)
        redis_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["file"])
