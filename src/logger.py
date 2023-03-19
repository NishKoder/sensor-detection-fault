import logging
import os
from datetime import datetime

from from_root import from_root

LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log"
logs_path = os.path.join(from_root(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] lineno-%(lineno)d  funcName-%(funcName)s %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
