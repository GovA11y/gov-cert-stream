# app/main.py
import certstream
import json
from utils import logger


def callback(message, context):

    logger.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            logger.info("No domains associated with this certificate")
        else:
            primary_domain = all_domains[0]
            if primary_domain.endswith('.gov') or primary_domain.endswith('.mil'):
                logger.info(f"Certificate issued for {primary_domain} by {context['source']['url']}")

certstream.listen_for_events(callback, url='wss://certstream.calidog.io/')
