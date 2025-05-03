from flask import jsonify
from app.services.database import get_db_connection

def get_diagnoses():
    query = "SELECT id_class AS id, name_class AS name FROM g_class_list"
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            diagnoses = cur.fetchall()
    return jsonify([{"id": d[0], "name": d[1]} for d in diagnoses]) 