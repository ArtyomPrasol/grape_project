from flask import jsonify, request
from app.services.database import get_db_connection
from app.services.storage import get_presigned_url

def get_requests():
    filters = {
        'id_user': request.args.get('id_user'),
        'diagnosis': request.args.get('diagnosis'),
        'start_date': request.args.get('start_date'),
        'end_date': request.args.get('end_date'),
    }

    query = """
    SELECT r.id_req, r.id_user, cl.name_class, cl2.name_class, r.date_create, r.file_name, rs.file_name_get 
    FROM g_request r
    JOIN g_request_spec rs on r.id_req = rs.id_req
    JOIN g_class_list cl on cl.id_class = rs.id_class
    LEFT JOIN g_class_list cl2 on cl2.id_class = r.id_comment_class
    WHERE 1=1"""

    params = []

    if filters['id_user']:
        query += " AND r.id_user = %s"
        params.append(filters['id_user'])

    if filters['diagnosis']:
        query += " AND cl.name_class = %s"
        params.append(filters['diagnosis'])

    if filters['start_date']:
        query += " AND r.date_create >= %s"
        params.append(filters['start_date'])

    if filters['end_date']:
        query += " AND r.date_create <= %s"
        params.append(filters['end_date'])

    query += " ORDER BY r.id_req desc"
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            requests = cur.fetchall()

    requests = [list(rec) for rec in requests]

    for rec in requests:
        if rec[5]:
            rec.append(get_presigned_url(rec[5]))
        if rec[6]:
            rec.append(get_presigned_url(rec[6]))

    reqsend = []
    for req in requests:
        req_data = {
            'id_req': req[0],
            'id_user': req[1],
            'diagnosis': req[2],
            'comment': req[3],
            'date_create': req[4],
            'file_name': req[5],
            'file_name_get': req[6],
            'file_url': req[7],
            'file_url_processed': req[8]
        }
        reqsend.append(req_data)

    return jsonify(reqsend) 