from google.cloud import bigquery

client = bigquery.Client.from_service_account_json('secrets/openweather-421711-1472594dde96.json')
# TODO(developer): Set table_id to the ID of the table to create.
table_id = "openweather-421711.air_pollution.pollution_1"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("co", "float"),
        bigquery.SchemaField("no", "float"),
        bigquery.SchemaField("no2", "float"),
    ],
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
)
uri = "gs://pollution_1"

load_job = client.load_table_from_uri(
    uri,
    table_id,
    location="europe-central2",  # Must match the destination dataset location.
    job_config=job_config,
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))