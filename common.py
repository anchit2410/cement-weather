import logging
from datetime import datetime    
import pytz  
import os
import uuid


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

latest_job_id = None

def flush_dir(output_dir, filename):
    try:
        if filename in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, filename))
    except Exception as e:
        LOGGER.error(f"flush_dir : exception : {e}")

def sanitize_path(path):
    return path.replace("\\","/")


# def get_current_datetime():
#     tz = pytz.timezone('Asia/Kolkata')
#     return datetime.now(tz)

def get_current_datetime(tz='Asia/Kolkata'):
    timezone = pytz.timezone(tz)   
    now = datetime.now(timezone)  
    return now.strftime("%d/%m/%Y-%H:%M:%S")

def get_job_id():
    return uuid.uuid4().hex
    
def format_numbers(x):
    try:
        return round(float(x), 2)
    except ValueError:
        return x
