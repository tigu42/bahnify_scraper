import logging
from datetime import datetime
logger = logging.getLogger(__name__)
logging.basicConfig(filename=f'bahnify{str(datetime.timestamp(datetime.now()))}.log', encoding='utf-8', level=logging.DEBUG)


def log_debug(m):
    logger.debug(m)

def log_normal(m):
    logger.info(m)

def log_critical(m):
    logger.error(m)