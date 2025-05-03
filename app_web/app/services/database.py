import psycopg2
from app.config import Config

def get_db_connection():
    return psycopg2.connect(
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    ) 