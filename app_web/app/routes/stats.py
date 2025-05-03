from flask import jsonify, request, send_file
from app.services.database import get_db_connection
from app.services.storage import get_object
import zipfile
from io import BytesIO

def stats():
    filters = {
        'id_user': request.args.get('id_user'),
        'diagnosis': request.args.get('diagnosis'),
        'start_date': request.args.get('start_date'),
        'end_date': request.args.get('end_date'),
    }

    query = """
    SELECT
      CASE
        WHEN r.id_comment_class IS NOT NULL
          AND r.level_trust IN (4,5)
        THEN cl_comm.name_class
        ELSE cl_spec.name_class
      END AS diagnosis,
      COUNT(*) AS count
    FROM g_request r
    JOIN g_request_spec rs
      ON r.id_req = rs.id_req
    JOIN g_class_list cl_spec
      ON cl_spec.id_class = rs.id_class
    LEFT JOIN g_class_list cl_comm
      ON cl_comm.id_class = r.id_comment_class
    WHERE TRUE
      AND cl_spec.id_class > 0
    """
    params = []

    if filters['id_user']:
        query += " AND r.id_user = %s"
        params.append(filters['id_user'])

    if filters['start_date']:
        query += " AND r.date_create >= %s"
        params.append(filters['start_date'])
    if filters['end_date']:
        query += " AND r.date_create <= %s"
        params.append(filters['end_date'])

    if filters['diagnosis']:
        query += """
        AND (
          (r.id_comment_class IS NOT NULL AND r.level_trust IN (4,5)
             AND cl_comm.name_class = %s)
          OR
          (NOT (r.id_comment_class IS NOT NULL AND r.level_trust IN (4,5))
             AND cl_spec.name_class = %s)
        )
        """
        params.extend([filters['diagnosis'], filters['diagnosis']])

    query += """
    GROUP BY diagnosis
    ORDER BY diagnosis;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()

    stats = [{'diagnosis': row[0], 'count': row[1]} for row in rows]
    return jsonify(stats)

def export_archive():
    query = """
        SELECT 
            rs.file_name_get,
            COALESCE(
                CASE 
                    WHEN r.id_comment_class IS NOT NULL AND u.level_trust >= 4 THEN cl_comment.name_class
                    ELSE NULL
                END,
                cl_spec.name_class
            ) AS class_name
        FROM g_request r
        JOIN g_user u ON r.id_user = u.id_user
        JOIN g_request_spec rs ON r.id_req = rs.id_req
        JOIN g_class_list cl_spec ON rs.id_class = cl_spec.id_class
        LEFT JOIN g_class_list cl_comment ON r.id_comment_class = cl_comment.id_class
        WHERE u.level_trust > 2
          AND rs.id_class > 0;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_name, class_name in results:
            try:
                response = get_object(file_name)
                file_data = response.read()
                response.close()
                response.release_conn()

                arc_path = f"{class_name}/{file_name.split('/')[-1]}"
                zipf.writestr(arc_path, file_data)

            except Exception as e:
                print(f"[!] Ошибка файла {file_name}: {e}")
                continue

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='grape_diagnoses.zip'
    ) 