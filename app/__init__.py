from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Load .env variables
load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Config
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')
    app.config['JWT_TOKEN_LOCATION'] = ["headers"]
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(weeks=5215)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=1)

    jwt.init_app(app)

    # CORS
    CORS(app, resources={
        r"/*": {
            "origins": os.getenv('FRONTEND_API_URL', '*'),
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Database Initialization
    from .models.database_connectivity import create_engine_session
    designer_engine, designer_session = create_engine_session('PRIMARY')

    from .routes import homepage, dashboard

    app.register_blueprint(homepage.homepage_bp)
    app.register_blueprint(dashboard.dashboard_bp)

    return app
