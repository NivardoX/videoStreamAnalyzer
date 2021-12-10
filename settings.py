import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent


with open('.cameras_config.json','r') as f:
    CAMERAS = json.load(f)

RABBIT_MQ_DEFAULT_URL = 'localhost:5672'
RABBIT_MQ_URL = os.environ.get("RABBIT_MQ_URL",RABBIT_MQ_DEFAULT_URL)


REDIS_DEFAULT_URL = 'localhost:6379'
REDIS_URL = os.environ.get("REDIS_URL",REDIS_DEFAULT_URL)

