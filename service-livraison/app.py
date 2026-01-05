import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from blueprint.commentaire_bp import commentaire_bp
from blueprint.livraison_bp import livraison_bp
from blueprint.statistique_bp import statistique_bp
from configs.config import db
from dotenv import load_dotenv

from seedeur.seedeur_init import seed_database

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

    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback_secret_key_change_in_production')
    print("🔑 JWT_SECRET_KEY utilisé :", os.environ.get('JWT_SECRET_KEY'))
    app.config['JWT_ALGORITHM'] = os.environ.get('JWT_ALGORITHM', 'HS256')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    jwt = JWTManager(app)
    database_url = os.environ.get('DATABASE_URL_LIVRAISON')
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


    # Blueprint
    app.register_blueprint(commentaire_bp)
    app.register_blueprint(livraison_bp)
    app.register_blueprint(statistique_bp)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return "Service livraison - Microservice"
    return app

if __name__ == '__main__':
    app = creation_app()
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, port=5001, host='0.0.0.0')