from minio import Minio
from minio.error import S3Error
from config import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, BUCKET_NAME
import os

def create_minio_client():
    """Создает и возвращает клиент MinIO"""
    client = Minio(
        MINIO_URL.replace("http://", "").replace("https://", ""),
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    
    # Проверяем существование бакета
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
    
    return client

def upload_file(client, file_path, object_name):
    """Загружает файл в MinIO"""
    try:
        with open(file_path, 'rb') as file_data:
            client.put_object(
                BUCKET_NAME,
                object_name,
                data=file_data,
                length=os.path.getsize(file_path),
                part_size=10 * 1024 * 1024
            )
        return True
    except S3Error as e:
        print(f"Error uploading file to MinIO: {str(e)}")
        return False

def get_file_url(client, object_name):
    """Возвращает URL файла в MinIO"""
    try:
        return client.presigned_get_object(BUCKET_NAME, object_name)
    except S3Error as e:
        print(f"Error getting file URL: {str(e)}")
        return None 