import os
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt


# Import des blueprints
from blueprint.auth_bp import auth_bp
from blueprint.client_bp import client_bp
from blueprint.livreur_bp import livreur_bp
from blueprint.manageur_bp import manageur_bp
from configs.config import db
from seeders.seed_roles import seed_database

load_dotenv()
migrate = Migrate()

def creation_app():
    app = Flask(__name__)

    # ✅ Configuration CORS
    CORS(app,
         supports_credentials=True,
         resources={r"*": {"origins": ["http://localhost:4200"]}},
         expose_headers=["Authorization"])

    # ✅ Configuration JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    print("🔑 JWT_SECRET_KEY utilisé :", os.environ.get('JWT_SECRET_KEY'))
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback_secret_key_change_in_production')

    app.config['JWT_ALGORITHM'] = os.environ.get('JWT_ALGORITHM', 'HS256')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    jwt = JWTManager(app)

    # Configuration de la base de données
    database_url = os.environ.get('DATABASE_URL_UTILISATEUR')
    if not database_url:
        raise ValueError("La variable DATABASE_URL n'est pas définie")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    # ✅ Callbacks JWT
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Token invalide", "error": str(error)}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Header Authorization manquant", "error": str(error)}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token expiré"}), 401

    # ✅ Enregistrement des blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(manageur_bp)
    app.register_blueprint(livreur_bp)

    # ✅ Routes santé
    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "utilisateur",
            "database": "connected" if database_url else "disconnected"
        })

    @app.route('/')
    def index():
        return "Service utilisateur - Microservice"

    # Création des tables
    with app.app_context():
        db.create_all()
        print("✅ Tables de base de données créées")

    return app


if __name__ == '__main__':
    app = creation_app()
    with app.app_context():
        db.create_all()
        seed_database()
    print("🚀 Service utilisateur démarré sur http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')
