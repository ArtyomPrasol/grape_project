from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from queue_processor import QueueProcessor
from routes import init_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Настройка JWT
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
    
    # Инициализация расширений
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    
    # Создание и запуск обработчика очереди
    queue_processor = QueueProcessor()
    queue_processor.start()
    
    # Инициализация маршрутов
    init_routes(app, queue_processor)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001) 