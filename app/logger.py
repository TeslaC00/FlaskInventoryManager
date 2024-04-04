import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define the log file and its maximum size
LOG_FILE = 'app.log'
MAX_BYTES = 1024 * 1024  # 1 MB

# Configure the logger to write to file
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_BYTES, backupCount=5)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Configure the logger to print to terminal
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
