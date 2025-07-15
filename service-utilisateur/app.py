from flask_jwt_extended import jwt_required, get_jwt

from services.crud_livreur import creation_livreur
from services.crud_manageur import creation_manageur
from services.crud_utilisateur import *
from services.authentification import *
from flask import Flask
from flask_migrate import Migrate
from configs.config import db

migrate= Migrate()

def creation_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/memoire_microservice_utilisateur'  # PostreSQL database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "admin"  # À changer en prod !
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return "service utilisateur"

    @app.route('/creer-un-compte', methods=["POST"])
    def creation_route():
        creation = creation_utilisateur()
        return creation

    @app.route('/supprimer-compte/<int:id>', methods=["POST"])
    def supprimer_route():
        archiver = archiver_utilisateur(id)
        return archiver

    @app.route('/modifier/<int:id>', methods=["POST"])
    def modifier_route():
        modifier = mettre_a_jour_utilisateur(id)
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

    return app
application = creation_app()

if __name__ == '__main__':
    application.run(debug=True, port=5000)
