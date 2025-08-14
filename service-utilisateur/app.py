import os

from flask_jwt_extended import JWTManager

from blueprint.auth_bp import auth_bp
from blueprint.client_bp import client_bp
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from blueprint.manageur_bp import manageur_bp
from configs.config import db

migrate= Migrate()

def creation_app():
    app = Flask(__name__)

    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
# 'postgresql://postgres:admin@localhost/memoire_microservice_utilisateur'
    database_url = os.environ.get('DATABASE_URL')
    print(f"Tentative de connexion à : {database_url}")  # Pour le débogage

    if not database_url:
        raise ValueError("La variable DATABASE_URL n'est pas définie")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "admin"  # À changer en prod !

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # Blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(manageur_bp)

    @app.route('/')
    def index():
        return "service utilisateur"

    return app

if __name__ == '__main__':
    application = creation_app()
    application.run(debug=True, port=5000, host='0.0.0.0')
