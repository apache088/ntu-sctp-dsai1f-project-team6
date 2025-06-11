import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# Configuration
project_id = os.getenv('DBT_PROJECT_ID')
dataset_id = os.getenv('DBT_PROJECT_DATASET')
table_name = 'raw_world_athletics'
csv_path = "../data/all_disciplines_combined.csv"

# Optional: Use a service account
# credentials = service_account.Credentials.from_service_account_file("path/to/your/service-account.json")
# client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

# If authenticated already, just use:
client = bigquery.Client(project=project_id)

# Define schema if needed (optional, BigQuery infers types otherwise)
# Useful for ensuring correct types, e.g., dates, floats, etc.
schema = [
    bigquery.SchemaField("rank", "INTEGER"),
    bigquery.SchemaField("mark", "STRING"),
    bigquery.SchemaField("wind", "FLOAT"),
    bigquery.SchemaField("competitor", "STRING"),
    bigquery.SchemaField("dob", "DATE"),
    bigquery.SchemaField("nationality", "STRING"),
    bigquery.SchemaField("position", "STRING"),
    bigquery.SchemaField("venue", "STRING"),
    bigquery.SchemaField("date", "DATE"),
    bigquery.SchemaField("result_score", "FLOAT"),
    bigquery.SchemaField("discipline", "STRING"),
    bigquery.SchemaField("type", "STRING"),
    bigquery.SchemaField("sex", "STRING"),
    bigquery.SchemaField("age_cat", "STRING"),
    bigquery.SchemaField("normalized_discipline", "STRING"),
    bigquery.SchemaField("track_field", "STRING"),
    bigquery.SchemaField("mark_numeric", "FLOAT"),
    bigquery.SchemaField("venue_country", "STRING"),
    bigquery.SchemaField("age_at_event", "FLOAT"),
    bigquery.SchemaField("season", "INTEGER"),
]

# Create dataset if it doesn’t exist
dataset_ref = client.dataset(dataset_id)
try:
    client.get_dataset(dataset_ref)
except Exception:
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"  # or "EU" depending on your project
    client.create_dataset(dataset, exists_ok=True)

# Load to BigQuery
table_id = f"{project_id}.{dataset_id}.{table_name}"
job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition="WRITE_TRUNCATE",  # Use WRITE_APPEND for incremental
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=False,
)

with open(csv_path, "rb") as source_file:
    load_job = client.load_table_from_file(source_file, table_id, job_config=job_config)

load_job.result()  # Waits for the job to finish
print(f"✅ Loaded {load_job.output_rows} rows to {table_id}")
