from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid
import os
from app.config import config
from app.redis.client import init_redis
from app.services.fileService import save_file

router = APIRouter()
# Initialize Redis client
redis_client = init_redis()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to the server.
    
    :param file: The file to upload.
    :return: A JSON response indicating success or failure.
    """
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400,
                detail="Only CSV files are allowed."
            )
        
        task_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        local_file_name = f"{task_id}{file_extension}"
        file_path = os.path.join(config.UPLOAD_FOLDER, local_file_name)

        if not save_file(file.file, file_path):
            raise HTTPException(status_code=500, detail="Failed to save file")
        
        redis_client.rpush(config.TASK_QUEUE, task_id)
        redis_client.hset(task_id, mapping={"status": "QUEUED", "file_path": file_path})
        
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "task_id": task_id})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("result/{task_id}")
async def get_result(task_id: str):
    """
    Get the result of a task.
    
    :param task_id: The ID of the task.
    :return: A JSON response containing the result of the task.
    """
    try:
        task = redis_client.hget(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found or expired")
        if task.status == "COMPLETED":
            with open(task.result_file_path, 'r') as result_file:
                return JSONResponse(status_code=200, content={"result": result_file.read()})
            return JSONResponse(status_code=200, content={"status": task.status, "error": task.error})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))