from app.redis.client import redis_client
import os
import csv
from app.config import config
from app.redis.client import init_redis
import time

redis_client = init_redis()


def save_file(file, file_path):
    """
    Save the uploaded file to the specified file path.

    :param file: The file object to save.
    :param file_path: The path where the file should be saved.
    :return: True if the file was saved successfully, False otherwise.
    """
    try:
        with open(file_path, "wb") as buffer:
            while chunk := file.read(4096):
                buffer.write(chunk)
        return True
    except Exception as e:
        return False


def delete_file(file_path):
    """
    Delete the file at the specified file path.

    :param file_path: The path of the file to delete.
    :return: True if the file was deleted successfully, False otherwise.
    """
    try:
        import os

        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        return False


def process_file(task_id, file_path):
    """
    Process the file at the specified file path.

    :param task_id: Redis key for tracking task state.
    :param file_path: The path of the file to process.
    """
    redis_client.hset(task_id, mapping={"status": "PROCESSING"})
    try:
        print(f"Processing file: {file_path}")
        print(f"Task ID: {task_id}")

        time.sleep(5)

        with open(file_path, "r", newline="") as csvfile:
            result = csv.reader(csvfile)
            header = next(result, None)
            row_count = sum(1 for _ in result)

        result_path = os.path.join(config.RESULTS_DIR, f"{task_id}.txt")
        with open(result_path, "w", newline="") as result_file:
            result_file.write(str(row_count))

        redis_client.hset(
            task_id, mapping={"status": "COMPLETED", "result_file_path": result_path}
        )

    except FileNotFoundError:
        redis_client.hset(
            task_id, mapping={"status": "FAILED", "error": "File not found"}
        )
    except Exception as e:
        redis_client.hset(task_id, mapping={"status": "FAILED", "error": str(e)})
    finally:
        if not delete_file(file_path):
            print(f"Warning: Failed to delete file: {file_path}")
