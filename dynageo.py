import logging
import logging.config
from typing import *

logging.config.fileConfig("etc/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("dynageo")

if __name__ == "__main__":
    logger.debug("Hello, world!")
