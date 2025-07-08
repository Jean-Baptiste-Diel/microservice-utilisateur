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

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
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

    return app
app = creation_app()

if __name__ == '__main__':
    app.run(debug=True)
