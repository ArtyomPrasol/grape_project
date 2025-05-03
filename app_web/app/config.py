class Config:
    JWT_SECRET_KEY = 'your_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Database settings
    DB_NAME = 'grape'
    DB_USER = 'AdminStore'
    DB_PASSWORD = '1234'
    DB_HOST = '150.241.75.156'
    DB_PORT = '5432'
    
    # MinIO settings
    MINIO_URL = "http://150.241.75.156:9000"
    MINIO_ACCESS_KEY = "grape_user"
    MINIO_SECRET_KEY = "grape2025pass"
    BUCKET_NAME = "grape" 