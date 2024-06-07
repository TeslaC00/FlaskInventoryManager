import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter  # Import ColoredFormatter from colorlog

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define the log file and its maximum size
LOG_FILE = 'app.log'
MAX_BYTES = 1024 * 1024  # 1 MB

# Configure the logger to write to file
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_BYTES, backupCount=5)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Configure the logger to print to terminal with color
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Use ColoredFormatter to add colors to log messages based on their severity level
color_formatter = ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
stream_handler.setFormatter(color_formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
