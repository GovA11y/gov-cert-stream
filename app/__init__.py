# app/__init__.py
import os
from .utils import logger
from dotenv import load_dotenv
import pyroscope
from .main import start_script  # Import start_script

load_dotenv()


def get_going():
    logger.info("Beginning Setup...")
    # Configure Pyroscope
    pyroscope.configure(
        application_name=os.getenv("PYROSCOPE_APPLICATION_NAME"),
        server_address=os.getenv("PYROSCOPE_SERVER"),
        auth_token=os.getenv("PYROSCOPE_AUTH_TOKEN"),
        tags={
            "host": "Bentley'sMacBookPro",
        },
    )

    logger.info('Pyroscope Configured')
    start_script()  # Call start_script
