"""
logger.py
Relative Path: app/utils/logger/logger.py

This module provides configuration for the logging system.

Author: TheBoatyMcBoatFace
"""
import os
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
import time
from logging.handlers import TimedRotatingFileHandler
from rich.logging import RichHandler

# Setup Sentry
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[sentry_logging],
    traces_sample_rate=1.0
)

logger_name = "GovA11y"
level = 'DEBUG'

# Set up logger:
logger = logging.getLogger(__name__)

# the handler determines where the logs go: stdout/file
shell_handler = shell_handler = RichHandler(markup=True)
filename = f"logs/{logger_name}-{time.strftime('%Y-%m-%d')}.log"
file_handler = TimedRotatingFileHandler(filename=filename, when="midnight", interval=1, backupCount=30)

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# the formatter determines what our logs will look like
fmt_shell = '%(message)s'
fmt_file = '%(asctime)s %(levelname)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# here we hook everything together
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)


def configure_logger():
    """
    Reconfigure the logger.

    This function reconfigures the logger with the predefined settings.
    """
    global logger
    logger = logging.getLogger(logger_name)


if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
