# app/utils/gcloud/bq_setup.py
from .auth import authenticate_bigquery
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import os

# Authenticate and Define the BigQuery client
client = authenticate_bigquery()

# Set the dataset and table name
dataset_name = os.getenv('GCLOUD_DATASET_NAME')
table_name = os.getenv('GCLOUD_BIGQUERY_TABLE')

# Define the schema
schema = [
    bigquery.SchemaField("Timestamp", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("Domain", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Issuer", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Issuer_Email", "STRING", mode="NULLABLE"),
]


def setup_table():
    # Check if the dataset exists
    dataset_ref = client.dataset(dataset_name)
    try:
        client.get_dataset(dataset_ref)
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset = client.create_dataset(dataset)
        print(f"Dataset {dataset_name} created.")

    # Check if the table exists
    table_ref = dataset_ref.table(table_name)
    try:
        client.get_table(table_ref)
    except NotFound:
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"Table {table.table_id} created.")

