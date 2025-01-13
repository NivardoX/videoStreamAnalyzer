import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent

with open(ROOT_DIR / '.cameras_config.json', 'r') as f:
    CAMERAS = json.load(f)

RABBIT_MQ_DEFAULT_URL = 'localhost:5672'
RABBIT_MQ_URL = os.environ.get("RABBIT_MQ_URL", RABBIT_MQ_DEFAULT_URL)

REDIS_DEFAULT_URL = 'localhost:6380'
REDIS_URL = os.environ.get("REDIS_URL", REDIS_DEFAULT_URL)

DATABSE_DEFAULT_URL = 'postgresql://postgres:postgres@127.0.0.1/stream_analyzer_db'
DATABSE_URL = os.environ.get("DATABSE_URL", DATABSE_DEFAULT_URL)
print(DATABSE_URL)
