from google.cloud import storage

def clear_bucket(credentials_path, bucket_name):
    client = storage.Client.from_service_account_json(credentials_path)
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()