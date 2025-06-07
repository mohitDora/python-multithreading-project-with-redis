from concurrent.futures import ThreadPoolExecutor
import os

executor = ThreadPoolExecutor(max_workers=os.cpu_count()*0.1)