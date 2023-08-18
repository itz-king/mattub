from . import *
from log import LOGGER

logger=LOGGER('initialising')

ultroid.start()
logger.info("Connecting DB")
logger.info("Connecting The Bot")
me=ultroid.get_entity("me")
logger.info(f"Connected Successfully As - {me.first_name} ({me.username})")
logger.info("Starting To Load Modules")
