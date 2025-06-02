from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    TASK_QUEUE = os.getenv('TASK_QUEUE')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    RESULTS_DIR = os.getenv('RESULTS_DIR', 'results')

config = Config()