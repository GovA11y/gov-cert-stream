# app/__init__.py
import os
from dotenv import load_dotenv
import sentry_sdk

# Load the .env file
load_dotenv()

from .utils import logger
import pyroscope
from .main import start_script
from .utils.gcloud import bq_setup


def get_going():
    logger.info("Beginning Setup...")
    # Configure Pyroscope
    pyroscope.configure(
        application_name=os.getenv("PYROSCOPE_APPLICATION_NAME"),
        server_address=os.getenv("PYROSCOPE_SERVER"),
        auth_token=os.getenv("PYROSCOPE_AUTH_TOKEN"),
        detect_subprocesses=False,
        oncpu=False,
        native=False,
        gil_only=True,
        tags={
            "host": "Bentley'sMacBookPro",
        },
    )

    # Get the Sentry DSN from environment variable
    sentry_dsn = os.getenv("SENTRY_DSN")
    if not sentry_dsn:
        raise EnvironmentError("SENTRY_DSN must be set in .env file.")

    # Initialize Sentry with the DSN from the environment variable
    sentry_sdk.init(
      dsn=sentry_dsn,
      # Set traces_sample_rate to 1.0 to capture 100%
      # of transactions for performance monitoring.
      # We recommend adjusting this value in production.
      traces_sample_rate=1.0
    )

    # Set up BigQuery table if not exists
    bq_setup.setup_table()

    logger.info('Pyroscope Configured')
    start_script()  # Call start_script

