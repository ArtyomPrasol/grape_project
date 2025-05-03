from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.routes import auth, requests, users, stats, diagnoses

def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Register routes
    app.route('/api/login', methods=['POST'])(lambda: auth.login(request.json))
    app.route('/api/requests', methods=['GET'])(requests.get_requests)
    app.route('/api/users', methods=['GET', 'POST'])(users.users)
    app.route('/api/confirm_user', methods=['POST'])(users.confirm_user)
    app.route('/api/stats', methods=['GET'])(stats.stats)
    app.route('/api/export_archive', methods=['GET'])(stats.export_archive)
    app.route('/api/diagnoses', methods=['GET'])(diagnoses.get_diagnoses)
    
    return app 