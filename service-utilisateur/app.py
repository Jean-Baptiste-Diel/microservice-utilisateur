import os

from flask_jwt_extended import jwt_required, get_jwt, JWTManager

from blueprint.auth import auth_bp
from services.crud.crud_livreur import creation_livreur
from services.crud.crud_manageur import creation_manageur
from services.crud.crud_utilisateur import *
from services.authentification import *
from services.service_commentaire import *
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from configs.config import db

migrate= Migrate()
# Blueprint?
def creation_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
    database_url = os.environ.get('DATABASE_URL')
    print(f"Tentative de connexion à : {database_url}")  # Pour le débogage

    if not database_url:
        raise ValueError("La variable DATABASE_URL n'est pas définie")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    app.config["JWT_SECRET_KEY"] = "admin"  # À changer en prod !
    jwt = JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return "service utilisateur"

    @app.route('/id/<int:livreur_id>,<int:client_id>', methods=["POST"])
    def id_route(livreur_id, client_id):
        pass
    @app.route('/creer-un-compte', methods=["POST"])
    def creation_route():
        creation = creation_utilisateur()
        return creation

    @app.route('/supprimer-compte/<int:id>', methods=["POST"])
    def supprimer_route():
        archiver = archiver_utilisateur(id)
        return archiver

    @app.route('/modifier/<int:id_utilisateur>', methods=["POST"])
    def modifier_route(id_utilisateur=None):
        modifier = mettre_a_jour_utilisateur(id_utilisateur)
        return modifier

    @app.route('/connexion', methods=["POST"])
    def connexion_route():
        connexion_utilisateur = connexion()
        return connexion_utilisateur

    @app.route('/deconnexion', methods=["POST"])
    def deconnexion_route():
        deconnexion_utilisateur = deconnexion()
        return deconnexion_utilisateur

    @app.route('/creation-manageur', methods=["POST"])
    def creation_manageur_route():
        creation_utilisateur_mangeur = creation_manageur()
        return creation_utilisateur_mangeur

    @app.route('/creation-livreur/<int:manageur_id>', methods=["POST"])
    @jwt_required()
    def creation_livreur_route(manageur_id):
        try:
            # 1. Vérification JWT et permissions
            claims = get_jwt()
            if claims.get('role') != 'Manageur' or claims.get('user_id') != manageur_id:
                return jsonify({"error": "Action non autorisée"}), 403
            # 2. Passe la main à la fonction de service
            return creation_livreur(manageur_id, request.get_json())
        except Exception as e:
            app.logger.error(f"Erreur route création livreur: {str(e)}")
            return jsonify({"error": "Erreur serveur"}), 500

    @app.route('/utilisateurs/<int:user_id>/commenter', methods=['POST'])
    def get_id_route():
        identifiants = get_id()
        return identifiants
    return app

application = creation_app()

if __name__ == '__main__':
    application.run(debug=True, port=5000, host='0.0.0.0')
