import logging
from logging.handlers import RotatingFileHandler
import sys

logging.basicConfig(
    level=logging.ERROR,  # Set the root logger to capture ERROR level and above
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "ub.log",
            mode="w",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler(sys.stderr)  # Log errors to stderr
    ]
)

def LOGGER(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger