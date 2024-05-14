import json
from google.cloud import storage
from geopy.geocoders import Nominatim
from airflow.models import Variable
import requests
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow import DAG

default_args=1
your_schedule_interval=[]
dag = DAG('your_dag_id', default_args=default_args, schedule_interval=your_schedule_interval)


def clear_bucket(credentials_path, bucket_name):
    client = storage.Client.from_service_account_json(credentials_path)
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()

def get_and_load_coordinates(cities, api_key, ti=None):
    geolocator = Nominatim(user_agent='myapplication')
    city_coordinates = {}

    for city in cities:
        location = geolocator.geocode(city)
        lat = location.latitude
        lon = location.longitude
        city_coordinates[city] = {"lat": lat, "lon": lon}

    cities_coordinates = json.dumps(city_coordinates)
    if ti is not None:
        ti.xcom_push(key='cities_coordinates', value=cities_coordinates)

def get_air_pollution(api_key, credentials_path, bucket_name, file_name, ti=None):
    if ti is not None:
        cities_coordinates = ti.xcom_pull(task_ids="fetch_coordinates", key="cities_coordinates")

        client = storage.Client.from_service_account_json(credentials_path)
        bucket = client.get_bucket(bucket_name)

        for city, coordinates in json.loads(cities_coordinates).items():
            lat = coordinates['lat']
            lon = coordinates['lon']
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            response = requests.get(url).json()
            data = json.dumps(response)
            blob = bucket.blob(f"{city}/{file_name}")
            blob.upload_from_string(data)

def upload_pollution_metrics_to_bigquery(credentials_path, table_id, uri, ti=None):
    load_to_bigquery = GCSToBigQueryOperator(
        task_id='load_to_bigquery',
        source_objects=[uri],
        source_format='json',
        destination_project_dataset_table=table_id,
        write_disposition='WRITE_TRUNCATE',
        skip_leading_rows=1,
        autodetect=True,
        google_cloud_storage_conn_id='google_cloud_default',
        bigquery_conn_id='google_cloud_default',
        dag=dag
    )
