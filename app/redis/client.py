from redis import Redis
from app.config import config
from redis import exceptions

redis_client = None


def init_redis():
    """Initialize the Redis client if not already initialized."""
    global redis_client
    if redis_client is None:
        try:
            redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
            redis_client.ping()
            print("Connected to Redis successfully.")
            return redis_client
        except exceptions.ConnectionError as e:
            redis_client = None
            print(f"Could not connect to Redis: {e}")
            return None
    return redis_client
