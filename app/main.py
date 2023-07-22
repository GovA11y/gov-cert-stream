# app/main.py
"""
Monitors certificate stream and logs information about .gov and .mil domains.
"""

import certstream
import time

from rich.console import Console
from rich.table import Table
from utils import logger

# Initialize the console
console = Console()

# Declare the time to wait between logs as a constant
TIME_BETWEEN_LOGS = 5 * 60


def log_status():
    """Logs a status message every hour."""
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

    # Print a status message every TIME_BETWEEN_LOGS
    if time.time() - callback.last_print_time > TIME_BETWEEN_LOGS:
        log_status()
        callback.last_print_time = time.time()

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            return

        primary_domain = all_domains[0]
        if primary_domain.endswith('.gov') or primary_domain.endswith('.mil'):
            logger.info(f"Certificate issued for {primary_domain} "
                        f"by {context['source']['url']}")
            cert_data = message['data']['leaf_cert']

            # Create a table to show details
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Key", style="dim")
            table.add_column("Value")

            table.add_row("Subject", cert_data['subject']['aggregated'])
            table.add_row("Not Before", str(cert_data['not_before']))
            table.add_row("Not After", str(cert_data['not_after']))
            table.add_row("Serial Number", cert_data['serial_number'])
            table.add_row("Fingerprint", cert_data['fingerprint'])
            console.print(table)


def on_error(instance, exception):
    """Logs an error message if the CertStreamClient instance fails."""
    logger.error(f"Exception in CertStreamClient! -> {str(exception)}")


# Initialize the last print time to now
callback.last_print_time = time.time()

logger.info("Starting to monitor certificate stream...")
certstream.listen_for_events(callback,
                             on_error=on_error,
                             url='wss://certstream.calidog.io/')
