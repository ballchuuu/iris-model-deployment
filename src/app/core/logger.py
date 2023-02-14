import logging
import sys

from app.core.config import settings

logger = logging.getLogger("gunicorn.error")
logger.setLevel(settings.log_level)

# to stream output to terminal
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
