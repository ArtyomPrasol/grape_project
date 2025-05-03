from flask import jsonify, request
from app.services.database import get_db_connection

def users():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            id_user = request.args.get('id_user')
            
            if request.method == 'POST':
                id_admin = request.args.get('id_admin')
                level_trust = request.args.get('level_trust')
                
                cur.execute(
                    "call log_trust_level_update(%s, %s, %s);",
                    (level_trust, id_admin, id_user)
                )
                conn.commit()
                return jsonify("Уровень доверия обновлен")

            if request.method == 'GET':
                if id_user:
                    cur.execute("""
                        SELECT id_user, first_name, last_name, level_trust, 
                               experience_year, confirment_exp, login
                        FROM g_user 
                        WHERE id_role = 1 AND id_user = %s;
                    """, (id_user,))
                else:
                    cur.execute("""
                        SELECT id_user, first_name, last_name, level_trust, 
                               experience_year, confirment_exp, login
                        FROM g_user 
                        WHERE id_role = 1;
                    """)
                
                users = cur.fetchall()
                reqsend = []
                
                for req in users:
                    req_data = {
                        'id_user': req[0],
                        'first_name': req[1],
                        'last_name': req[2],
                        'level_trust': req[3],
                        'experience_year': req[4],
                        'confirment_exp': req[5].isoformat() if req[5] else None,
                        'login': req[6]
                    }
                    reqsend.append(req_data)
                    
                return jsonify(reqsend)

def confirm_user():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            id_user = request.args.get('id_user')
            id_admin = request.args.get('id_admin')
            experience_year = request.args.get('experience_year')
            
            if not all([id_user, id_admin, experience_year]):
                return jsonify({"error": "Не все необходимые параметры указаны"}), 400
            
            try:
                cur.execute(
                    """
                    UPDATE g_user 
                    SET experience_year = %s, 
                        confirment_exp = CURRENT_TIMESTAMP 
                    WHERE id_user = %s;
                    """,
                    (experience_year, id_user)
                )
                conn.commit()
                return jsonify({"message": "Пользователь успешно подтвержден"})
                
            except Exception as e:
                conn.rollback()
                return jsonify({"error": str(e)}), 500 