# Python Multithreading Project with Redis

This project demonstrates a file processing system using Python multithreading, Redis for task management, and FastAPI for the API layer. It allows users to upload CSV files, processes them in the background, and provides results via an API.

## Features
- **FastAPI**: REST API for file upload and result retrieval
- **Redis**: Task queue and state management
- **Multithreading**: Background processing of file tasks
- **File Handling**: Upload, process, and clean up CSV files

## Project Structure
- `app/api/file.py`: API endpoints for file upload and result retrieval
- `app/services/fileService.py`: File operations and processing logic
- `app/services/consumerService.py`: Background consumer for processing tasks
- `app/services/threadService.py`: Thread pool executor setup
- `app/redis/client.py`: Redis client initialization
- `app/config.py`: Configuration management

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   - Create a `.env` file in the root directory with the following (or use defaults):
     ```env
     REDIS_HOST=localhost
     REDIS_PORT=6379
     TASK_QUEUE=task_queue
     UPLOAD_FOLDER=uploads
     RESULTS_DIR=results
     ```
4. **Start Redis server** (if not already running)
5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage
- **Upload a CSV file**: `POST /api/upload` with a file
- **Check result**: `GET /api/result/{task_id}`

## Notes
- Only CSV files are accepted for upload.
- Processed results are stored in the `results` directory.
- Tasks and their statuses are managed in Redis.

## License
MIT 