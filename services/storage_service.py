from google.cloud import storage

def upload_audio_to_gcs(local_file_path: str, bucket_name: str, destination_blob_name: str) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    #blob.make_public()  # Opcional: hace el archivo accesible públicamente

    return blob.public_url
