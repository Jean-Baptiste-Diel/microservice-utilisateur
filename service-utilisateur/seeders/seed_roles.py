from models import Role
from app import db, creation_app

app = creation_app()

with app.app_context():
    # Création des rôles
    roles = [
        Role(nom_du_role="Admin"),
        Role(nom_du_role="Utilisateur"),
        Role(nom_du_role="Manageur"),
        Role(nom_du_role="Livreur")
    ]
    db.session.add_all(roles)
    db.session.commit()
    print("initialisation terminé !")