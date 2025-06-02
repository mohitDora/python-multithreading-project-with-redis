import threading
from app.redis.client import init_redis
from app.config import config
from app.services.threadService import executor
from app.services.fileService import proccess_file

redis_client = init_redis()
stop_event = threading.Event()

def consumer_service():
    while not stop_event.is_set():
        task=redis_client.blpop(config.TASK_QUEUE)
        if task:
            _,task_id = task
            file_path=redis_client.hget(task_id, 'file_path')
            if file_path:
                executor.submit(proccess_file, task_id, file_path)
            else:
                redis_client.hset(task_id, mapping={"status": "FAILED", "error": "File not found"})
        else:
            pass
