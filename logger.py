import logging
import sys

from config import LOG_PATH

LOGGER_FORMAT = '[%(asctime)s]: [%(levelname)s]: [%(message)s]'
DATE_FORMAT = '%d.%m.%Y %H:%M:%S'

logger = logging.getLogger('webserver')
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(logging.Formatter(fmt=LOGGER_FORMAT, datefmt=DATE_FORMAT))

file_handler = logging.FileHandler(filename=LOG_PATH)
file_handler.setFormatter(logging.Formatter(fmt=LOGGER_FORMAT, datefmt=DATE_FORMAT))

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
