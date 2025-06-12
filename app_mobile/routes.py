from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import datetime
import os
from database import Database
from minio_storage import create_minio_client, get_file_url, upload_file
from queue_processor import QueueProcessor
from config import REQ_FOLDER, BUCKET_NAME
from utils import remove_extension

def init_routes(app, queue_processor):
    db = Database()
    minio_client = create_minio_client()

    @app.route('/request', methods=['POST'])
    def post_request():
        try:
            photo = request.files.get('photo')
            id_client = request.form.get('id_client')
            filename = f"{id_client}_{datetime.today().year}_{int((datetime.now() - datetime(datetime.now().year, 1, 1)).total_seconds() * 1000)}.jpg"

            # Сохраняем файл локально
            photo_path = os.path.join(REQ_FOLDER, filename)
            photo.save(photo_path)

            # Загружаем файл в MinIO используя существующую функцию
            if not upload_file(minio_client, photo_path, filename):
                raise Exception("Failed to upload file to MinIO")

            # Добавляем запрос в базу данных
            request_id = db.add_request(id_client, filename)
            queue_processor.add_task(request_id, filename)

            return jsonify({'message': f'Data saved with ID: {id_client}, Image: {filename}'})
        except Exception as e:
            db.conn.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/user/<int:id_client>/request', methods=['GET'])
    def get_client_requests(id_client):
        try:
            cur = db.conn.cursor()
            cur.execute(f"""SELECT 
                r.file_name,  
                r.date_create,
                rs.date_create,
                r.id_comment_class,
                cl2.name_class
                FROM g_request r 
                LEFT JOIN g_request_spec rs on r.id_req = rs.id_req
                LEFT JOIN g_class_list cl1 on cl1.id_class = r.id_comment_class
                LEFT JOIN g_class_list cl2 on cl2.id_class = rs.id_class
                WHERE r.id_user = {id_client}
                ORDER BY r.id_req""")
            data = cur.fetchall()
            cur.close()

            result = [
                {
                    "code_name" : remove_extension(row[0]),
                    "date_create" : row[1],
                    "time_get" : row[2],
                    "class_comment" : row[3],
                    "class_set" : row[4]
                }
                for row in data 
            ]
        
            return jsonify(result)
        except Exception as e:
            db.conn.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/register', methods=['POST'])
    def register():
        try:
            login = request.form.get("login")
            password = request.form.get("password")

            cur = db.conn.cursor()
            cur.execute(f"INSERT INTO g_user (login, password) VALUES ('{login}', '{password}') RETURNING id_user")
            user_id = cur.fetchone()[0]
            db.conn.commit()
            cur.close()

            return jsonify({'message': 'User registered successfully', 'user_id': user_id})
        except Exception as e:
            db.conn.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/login', methods=['POST'])
    def login():
        try:
            login = request.form.get("login")
            password = request.form.get("password")

            cur = db.conn.cursor()
            cur.execute(f"SELECT id_user FROM g_user WHERE login = '{login}' AND password = '{password}'")
            user = cur.fetchone()
            cur.close()

            if not user:
                return jsonify({"error": "Неверный логин или пароль"}), 401
            
            return jsonify({"user_id": user[0]}), 200
        except Exception as e:
            db.conn.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/get_classes', methods=['GET'])
    def get_classes_api():
        try:
            class_list = db.get_classes()
            return jsonify({
                'classes': class_list
            })
        except Exception as e:
            db.conn.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/user', methods=['GET'])
    def get_user():
        try:
            user_id = request.args.get('id_user')
            if not user_id:
                return jsonify({"error": "id_user не указан"}), 400

            cur = db.conn.cursor()
            cur.execute("SELECT first_name, last_name, login, experience_year FROM g_user WHERE id_user = %s", (user_id,))
            user_data = cur.fetchone()
            cur.close()

            if not user_data:
                return jsonify({"error": "Пользователь не найден"}), 404

            result = {
                "first_name": user_data[0],
                "last_name": user_data[1],
                "login": user_data[2],
                "experience_year": user_data[3]
            }
            return jsonify(result), 200

        except Exception as e:
            db.conn.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route('/update_user', methods=['PUT'])
    def update_user():
        try:
            data = request.get_json()
            user_id = data.get('id_user')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            password = data.get('password')
            experience_year = data.get('experience_year')

            if not user_id:
                return jsonify({"error": "id_user не указан"}), 400

            cur = db.conn.cursor()
            if password:
                cur.execute("""
                    UPDATE g_user
                    SET first_name = %s,
                        last_name = %s,
                        password = %s,
                        experience_year = %s
                    WHERE id_user = %s
                """, (first_name, last_name, password, experience_year, user_id))
            else:
                cur.execute("""
                    UPDATE g_user
                    SET first_name = %s,
                        last_name = %s,
                        experience_year = %s
                    WHERE id_user = %s
                """, (first_name, last_name, experience_year, user_id))

            db.conn.commit()
            cur.close()

            return jsonify({"message": "Профиль успешно обновлён"}), 200

        except Exception as e:
            db.conn.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route("/get_url")
    def get_image_url():
        code_name = request.args.get("code_name") + ".jpg"
        try:
            url = get_file_url(minio_client, code_name)
            return jsonify({"url": url})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/send_class', methods=['POST'])
    def send_class():
        try:
            data = request.get_json()
            code_name = data.get("code_name")
            id_class = data.get("id_class")

            if not code_name or not id_class:
                return jsonify({"error": "Не указаны все данные"}), 400

            cur = db.conn.cursor()
            cur.execute("call set_class_comment(%s,%s)", (id_class, code_name))
            db.conn.commit()
            cur.close()

            return jsonify({"success": True})

        except Exception as e:
            db.conn.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route('/stats', methods=['GET'])
    def stats():
        try:
            filters = {
                'id_user': request.args.get('id_user'),
                'diagnosis': request.args.get('diagnosis'),
                'start_date': request.args.get('start_date'),
                'end_date': request.args.get('end_date'),
            }

            params = []
            query = ""
            cur = db.conn.cursor()

            if filters['diagnosis'] and filters['diagnosis'] != "Не выбран":
                query = """
                    SELECT TO_CHAR(r.date_create, 'YYYY-MM-DD') AS day, COUNT(*) AS count
                    FROM g_request r
                    LEFT JOIN g_request_spec rs ON r.id_req = rs.id_req
                    JOIN g_class_list cl ON cl.id_class = COALESCE(r.id_comment_class, rs.id_class)
                    WHERE cl.name_class = %s
                """
                params.append(filters['diagnosis'])

                if filters['id_user']:
                    query += " AND r.id_user = %s"
                    params.append(filters['id_user'])

                if filters['start_date']:
                    query += " AND r.date_create >= %s"
                    params.append(filters['start_date'])

                if filters['end_date']:
                    query += " AND r.date_create <= %s"
                    params.append(filters['end_date'])

                query += " GROUP BY day ORDER BY day"

                cur.execute(query, tuple(params))
                rows = cur.fetchall()

                result = [{'date': row[0], 'count': row[1]} for row in rows]
                return jsonify({'mode': 'by_date', 'data': result}), 200

            query = """
                SELECT cl.name_class, COUNT(*) AS count
                FROM g_request r
                LEFT JOIN g_request_spec rs ON r.id_req = rs.id_req
                JOIN g_class_list cl ON cl.id_class = COALESCE(r.id_comment_class, rs.id_class)
                WHERE 1=1
            """

            if filters['id_user']:
                query += " AND r.id_user = %s"
                params.append(filters['id_user'])

            if filters['start_date']:
                query += " AND r.date_create >= %s"
                params.append(filters['start_date'])

            if filters['end_date']:
                query += " AND r.date_create <= %s"
                params.append(filters['end_date'])

            query += " GROUP BY cl.name_class ORDER BY count DESC"

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            result = [{'diagnosis': row[0], 'count': row[1]} for row in rows]
            return jsonify({'mode': 'by_diagnosis', 'data': result}), 200

        except Exception as e:
            db.conn.rollback()
            return jsonify({"error": str(e)}), 500 