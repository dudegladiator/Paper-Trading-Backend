import logging
from logging.handlers import RotatingFileHandler
from utils.logger_api import NewRelicHandler
from utils.IST_Time import get_current_time_IST
from dotenv import load_dotenv
import os
load_dotenv()


class ContextFilter(logging.Filter):
    """
    Custom logging filter to add api_key and log_type to log records.
    """
    def __init__(self, api_key=None, log_type=None, name=None):
        super().__init__()
        self.api_key = api_key
        self.log_type = log_type
        self.name = name

    def filter(self, record):
        record.api_key = self.api_key if self.api_key else 'unknown'
        record.log_type = self.log_type if self.log_type else 'unknown'
        record.name = self.name if self.name else 'unknown'
        return True

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define a custom log format
log_format_file = '%(asctime)s - %(message)s'

# Create a rotating file handler with a maximum file size of 1 MB and 10 backup files
# file_handler = RotatingFileHandler('database.log', maxBytes=1024*1024, backupCount=10)
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(logging.Formatter(log_format_file))

# # Add the rotating file handler to the logger
# logger.addHandler(file_handler)

# Add NewRelicHandler to the logger
api_key = os.getenv("LOG_KEY")  # Replace with your New Relic API key
new_relic_handler = NewRelicHandler(api_key)
new_relic_handler.setLevel(logging.INFO)
new_relic_handler.setFormatter(logging.Formatter(log_format_file))

logger.addHandler(new_relic_handler)

def log_creator(api_key, name, log, error=False):
    if error:
        log_type = "ERROR"
    else:
        log_type = "INFO"
    context_filter = ContextFilter(api_key=api_key, log_type=log_type, name=name)
    logger.addFilter(context_filter)
    if error:
        logging.error(log)
    else:
        logging.info(log)
    logger.removeFilter(context_filter)


if __name__ == "__main__":
    log_creator("user123456", "harsh", "Test log message", error=False)
