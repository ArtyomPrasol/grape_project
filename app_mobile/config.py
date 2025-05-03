import os
from datetime import timedelta
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# MinIO Configuration
MINIO_URL = os.getenv('MINIO_URL', 'http://150.241.75.156:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'grape_user')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'grape2025pass')
BUCKET_NAME = os.getenv('BUCKET_NAME', 'grape')

# Database Configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'grape'),
    'user': os.getenv('DB_USER', 'AdminStore'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'host': os.getenv('DB_HOST', '150.241.75.156'),
    'port': os.getenv('DB_PORT', '5432')
}

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))

# File Paths
REQ_FOLDER = r'static/request'
DONE_FOLDER = r'static/request_done'
ASSETS_FOLDER = r'static/assets'

# Model Files
MODEL = 'GrapeMax4_Model.hdf5'
YOLO_MODEL_NAME = 'best.pt'

# Create necessary directories
os.makedirs(REQ_FOLDER, exist_ok=True)
os.makedirs(DONE_FOLDER, exist_ok=True)
os.makedirs(ASSETS_FOLDER, exist_ok=True) 