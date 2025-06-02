from app.redis.client import redis_client
import os
import csv
from app.config import config
from app.redis.client import init_redis

redis_client=init_redis()

def save_file(file, file_path):
    """
    Save the uploaded file to the specified file path.
    
    :param file: The file object to save.
    :param file_path: The path where the file should be saved.
    :return: True if the file was saved successfully, False otherwise.
    """
    try:
        with open(file_path, 'wb') as buffer:
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
    
def proccess_file(task_id, file_path):
    """
    Process the file at the specified file path.
    
    :param file_path: The path of the file to process.
    """
    redis_client.hset('task_status', task_id, 'PROCESSING')
    try:
        row_count = 0
        import time
        time.sleep(5)  # Simulate a delay for processing
        #store result in local
        with open(file_path, 'r') as csvfile:
            result = csv.reader(csvfile)
            header = next(result,None)
            for _ in result:
                row_count += 1
            row_count = row_count - 1 if header else row_count
        with open(f"{config.RESULTS_DIR}/{task_id}.txt", 'w', newline='') as result_file:
            result_file.write(f"{row_count}")
        redis_client.hset(task_id, mapping={"status": "COMPLETED", "result_file_path": f"{config.RESULTS_DIR}/{task_id}.txt"})
    except FileNotFoundError:
        redis_client.hset(task_id, mapping={"status": "FAILED", "error": "File not found"})
    except Exception as e:
        redis_client.hset(task_id, mapping={"status": "FAILED", "error": str(e)})
    finally:
        if not delete_file(file_path):
            raise Exception("Failed to delete file")