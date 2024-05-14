from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from utils import clear_bucket, get_and_load_coordinates, get_air_pollution, upload_pollution_metrics_to_bigquery

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('air_pollution_data_pipeline', default_args=default_args, schedule_interval=timedelta(hours=1), catchup=False) as dag:
    start = EmptyOperator(task_id='start')

    fetch_coordinates = PythonOperator(
        task_id='fetch_coordinates',
        python_callable=get_and_load_coordinates,
        op_kwargs={'cities': ['Bydgoszcz', 'Gdańsk', 'Katowice', 'Kraków', 'Lublin', 'Poznań', 'Szczecin', 'Warszawa', 'Wrocław', 'Lublin'],
                   'api_key': "{{ var.value.OPENWEATHER_API_KEY }}"},
        provide_context=True,
    )

    fetch_pollution_data = PythonOperator(
        task_id='fetch_pollution_data',
        python_callable=get_air_pollution,
        op_kwargs={'api_key': "{{ var.value.OPENWEATHER_API_KEY }}",
                   'credentials_path': "/path/to/google_cloud_service_key.json",
                   'bucket_name': "your_bucket_name",
                   'file_name': "pollution_data.json"},
        provide_context=True,
    )

    upload_to_bigquery = PythonOperator(
        task_id='upload_to_bigquery',
        python_callable=upload_pollution_metrics_to_bigquery,
        op_kwargs={'credentials_path': "/path/to/google_cloud_service_key.json",
                   'table_id': "your_project_id.your_dataset_id.your_table_id",
                   'uri': "gs://your_bucket_name/pollution_data.json"},
        provide_context=True,
    )

    end = EmptyOperator(task_id='end')

    start >> fetch_coordinates >> fetch_pollution_data >> upload_to_bigquery >> end
