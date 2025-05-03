import psycopg2
from config import DB_CONFIG
from utils import list_to_dict

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.class_list = {}
        self.bind_class_model = {}
        self._load_classes()

    def _load_classes(self):
        """Загружает список классов из базы данных"""
        cur = self.conn.cursor()
        cur.execute("SELECT id_class, name_class FROM g_class_list")
        class_list_mas = cur.fetchall()
        self.class_list = list_to_dict(class_list_mas)
        
        cur.execute("SELECT id_code, id_class FROM g_class_in_model")
        bind_class_model_mas = cur.fetchall()
        self.bind_class_model = list_to_dict(bind_class_model_mas)
        cur.close()

    def get_classes(self):
        """Возвращает список классов и их привязки к модели"""
        return self.class_list

    
    def get_classes_bind(self):
        """Возвращает список классов и их привязки к модели"""
        return self.bind_class_model
    
    def add_request(self, user_id, filename):
        """Добавляет новый запрос в базу данных"""
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO g_request (id_user, file_name) VALUES ({user_id},'{filename}') RETURNING id_req")
        request_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return request_id

    def update_request_status(self, request_id, class_id, filename):
        """Обновляет статус запроса"""
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO g_request_spec (id_req, id_class, file_name_get) VALUES ({request_id}, {class_id}, '{filename}')")
        cur.execute(f"CALL user_req_post({request_id}, 1)")
        self.conn.commit()
        cur.close()

    def close(self):
        """Закрывает соединение с базой данных"""
        self.conn.close() 