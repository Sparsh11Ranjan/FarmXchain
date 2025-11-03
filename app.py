import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'dev-secret'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or 'jwt-dev-secret'

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": os.getenv('CORS_ORIGINS', '*')}})

    from routes.auth import auth_bp
    from routes.farmers import farmers_bp
    from routes.products import products_bp
    from routes.farming import farming_bp
    from routes.records import records_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(farmers_bp, url_prefix='/api/farmers')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(farming_bp, url_prefix='/api/farming-types')
    app.register_blueprint(records_bp, url_prefix='/api/records')

    @app.route('/api/test', methods=['GET'])
    def test_connection():
        try:
            from models import Test
            Test.query.first()
            return jsonify({'message': 'Database connection successful'}), 200
        except Exception as e:
            app.logger.error('DB connection failed: %s', e)
            return jsonify({'error': 'Database connection failed'}), 500

    return app