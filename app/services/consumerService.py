import threading
from app.redis.client import init_redis
from app.config import config
from app.services.threadService import executor
from app.services.fileService import process_file
import traceback

redis_client = init_redis()
stop_event = threading.Event()

def consumer_service():
    while not stop_event.is_set():
        try:
            task = redis_client.blpop(config.TASK_QUEUE)

            if task:
                decoded_task_id = task[1].decode("utf-8")
                print(f"Processing task: {decoded_task_id}")
                file_path = redis_client.hget(decoded_task_id, "file_path")
                if file_path is not None:
                    file_path = file_path.decode("utf-8")
                    executor.submit(process_file, decoded_task_id, file_path)
                else:
                    redis_client.hset(
                        decoded_task_id,
                        mapping={"status": "FAILED", "error": "File not found"},
                    )
            else:
                pass
        except Exception as e:
            print(f"Error in consumer_service: {e}")
            traceback.print_exc()
