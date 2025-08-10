import os

from flask_jwt_extended import JWTManager

from blueprint.auth_bp import auth_bp
from blueprint.client_bp import client_bp
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from configs.config import db

migrate= Migrate()

def creation_app():
    app = Flask(__name__)

    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

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
    print("===== ROUTES ENREGISTRÉES =====")
    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(rule.methods))
        print(f"{rule.rule}  [{methods}]")
    print("====")

    @app.route('/')
    def index():
        return "service utilisateur"

    return app
application = creation_app()
if __name__ == '__main__':

    application.run(debug=True, port=5000, host='0.0.0.0')
