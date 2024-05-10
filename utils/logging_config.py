import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

def setup_logging():
    log_directory = os.path.join('storage', 'logs')
    log_filename = os.path.join(log_directory, 'bot.log')

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging.basicConfig(
        level=logging.getLevelName(log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=5),
            logging.StreamHandler()
        ]
    )
