from google.cloud import storage
from datetime import timedelta

from src.core.config import get_settings

settings = get_settings()

GCS_BUCKET_NAME = settings.GCS_BUCKET_NAME


class GoogleCloudStorage:
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(GCS_BUCKET_NAME)

    def upload_to_gcs(self, file_stream, filename, content_type):
        destination_blob_name = f"uploads/{filename}"
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_file(file_stream, content_type=content_type)

        return destination_blob_name

    def generate_signed_url(self, object_name: str, expiration_minutes: int = 15):
        blob = self.bucket.blob(object_name)

        url = blob.generate_signed_url(
            version="v4", expiration=timedelta(minutes=expiration_minutes), method="GET"
        )
        return url
