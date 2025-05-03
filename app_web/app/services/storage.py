from minio import Minio
from datetime import timedelta
from app.config import Config

minio_client = Minio(
    Config.MINIO_URL.replace("http://", "").replace("https://", ""),
    access_key=Config.MINIO_ACCESS_KEY,
    secret_key=Config.MINIO_SECRET_KEY,
    secure=False
)

def get_presigned_url(file_name, expires=timedelta(hours=1)):
    return minio_client.presigned_get_object(
        Config.BUCKET_NAME, file_name, expires=expires
    )

def get_object(file_name):
    return minio_client.get_object(Config.BUCKET_NAME, file_name) 