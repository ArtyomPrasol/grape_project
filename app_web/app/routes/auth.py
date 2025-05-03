from flask import jsonify
from flask_jwt_extended import create_access_token
from app.services.database import get_db_connection

def login(data):
    username = data['username']
    password = data['password']

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id_user FROM g_user WHERE login = %s AND password = %s AND id_role = 2",
                (username, password)
            )
            user = cur.fetchone()

    if user:
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token, "client": user}), 200

    return jsonify({"msg": "Invalid username or password"}), 401 