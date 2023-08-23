import certstream
import time
import pyroscope
import os

from rich.console import Console
from .utils import logger, gcloud_auth

client = gcloud_auth()
# Get the table reference
dataset_name = os.getenv('GCLOUD_DATASET_NAME')
table_name = os.getenv('GCLOUD_BIGQUERY_TABLE')
table_ref = client.dataset(dataset_name).table(table_name)
table = client.get_table(table_ref)

# Declare the time to wait between logs as a constant
TIME_BETWEEN_LOGS = 5 * 60

# Initialize the console
console = Console()


def log_status():
    """Logs a status message every hour."""
    with pyroscope.tag_wrapper({"function": "log_status"}):
        while True:
            logger.info("Still monitoring the certificate stream...")
            time.sleep(60 * 60)


def callback(message, context):
    """
    Callback function for handling certificate updates.

    Args:
        message: The message data from the certificate update.
        context: The context data from the certificate update.
    """
    with pyroscope.tag_wrapper({"function": "callback"}):

        # Print a status message every TIME_BETWEEN_LOGS
        if time.time() - callback.last_print_time > TIME_BETWEEN_LOGS:
            log_status()
            callback.last_print_time = time.time()

        if message['message_type'] == "certificate_update":
            all_domains = message['data']['leaf_cert']['all_domains']
            issuer = message['data']['leaf_cert']['issuer']

            if len(all_domains) == 0:
                return

            # Iterate over all domains in the certificate
            for domain in all_domains:
                if domain.endswith('.gov') or domain.endswith('.mil'):
                    issuer_name = issuer['aggregated']
                    issuer_email = issuer.get('emailAddress')  # Can be null

                    # Log the timestamp, domain, issuer, and issuer email address
                    logger.info(f"Timestamp: {message['data']['seen']} \n"
                                f"Domain: {domain} \n"
                                f"Issuer: {issuer_name} \n"
                                f"Issuer Email: {issuer_email}")

                    # Create a row object to insert into BigQuery
                    row_to_insert = {
                        "timestamp": message['data']['seen'],
                        "domain": domain,
                        "issuer": issuer_name,
                        "issuer_email": issuer_email
                    }

                    # Insert the row into BigQuery
                    errors = client.insert_rows(table, [row_to_insert])

                    # If any errors occurred, log them
                    if errors:
                        logger.error(errors)


def on_error(instance, exception):
    """Logs an error message if the CertStreamClient instance fails."""
    with pyroscope.tag_wrapper({"function": "on_error"}):
        logger.error(f"Exception in CertStreamClient! -> {str(exception)}")


def start_script():
    with pyroscope.tag_wrapper({"function": "start_script"}):
        # Initialize the last print time to now
        callback.last_print_time = time.time()

        logger.info("Starting to monitor certificate stream...")
        certstream.listen_for_events(callback,
                                     on_error=on_error,
                                     url='wss://certstream.calidog.io/')
