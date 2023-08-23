# app/utils/gcloud/auth.py
from google.oauth2 import service_account
from google.cloud import bigquery
from ..monitoring import logger
import os

def authenticate_bigquery():
    # Path to the service account key file, which you can set as an environment variable
    key_path = os.getenv('GCLOUD_SERVICE_KEY_PATH')
    logger.debug(f'Key Path: {key_path}')

    if not key_path:
        raise EnvironmentError('GCLOUD_SERVICE_KEY_PATH must be set to the path of the service account key file.')

    if not os.path.exists(key_path):
        raise FileNotFoundError(f'Service account key file {key_path} not found.')

    # Use the key file to authenticate
    credentials = service_account.Credentials.from_service_account_file(key_path)

    # Create a BigQuery client with the credentials
    client = bigquery.Client(credentials=credentials)

    return client
