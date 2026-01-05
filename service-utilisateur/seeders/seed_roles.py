from datetime import datetime, timezone
from configs.config import db
import bcrypt  # Remplacement de werkzeug.security par bcrypt

from models import Role, Utilisateur, Manageur, Livreur, Client

def hash_password(password):
    """Hash un mot de passe avec bcrypt"""
    # Générer un salt et hasher le mot de passe
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def seed_database():
    """Fonction pour peupler la base de données avec des données initiales"""

    # Vérifier si les rôles existent déjà
    if Role.query.count() == 0:
        print("Création des rôles...")

        # Création des rôles
        roles = [
            Role(nom_du_role="Administrateur"),
            Role(nom_du_role="Manageur"),
            Role(nom_du_role="Livreur"),
            Role(nom_du_role="Client")
        ]

        for role in roles:
            db.session.add(role)

        db.session.commit()

    # Vérifier si les utilisateurs existent déjà
    if Utilisateur.query.count() == 0:
        print("Création des utilisateurs...")

        # Récupérer les rôles
        admin_role = Role.query.filter_by(nom_du_role="Administrateur").first()
        manageur_role = Role.query.filter_by(nom_du_role="Manageur").first()
        livreur_role = Role.query.filter_by(nom_du_role="Livreur").first()
        client_role = Role.query.filter_by(nom_du_role="Client").first()

        # Création des utilisateurs avec bcrypt
        utilisateurs = [
            # Administrateur
            Utilisateur(
                nom="Admin",
                prenom="System",
                email="admin@example.com",
                mot_de_passe=hash_password("admin123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=admin_role.id
            ),

            # Manageurs
            Utilisateur(
                nom="Dupont",
                prenom="Marie",
                email="marie.dupont@example.com",
                mot_de_passe=hash_password("manageur123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=manageur_role.id
            ),
            Utilisateur(
                nom="Martin",
                prenom="Pierre",
                email="pierre.martin@example.com",
                mot_de_passe=hash_password("manageur123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=manageur_role.id
            ),

            # Livreurs
            Utilisateur(
                nom="Bernard",
                prenom="Luc",
                email="luc.bernard@example.com",
                mot_de_passe=hash_password("livreur123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=livreur_role.id
            ),
            Utilisateur(
                nom="Petit",
                prenom="Sophie",
                email="sophie.petit@example.com",
                mot_de_passe=hash_password("livreur123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=livreur_role.id
            ),
            Utilisateur(
                nom="Robert",
                prenom="Jean",
                email="jean.robert@example.com",
                mot_de_passe=hash_password("livreur123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=livreur_role.id
            ),

            # Clients
            Utilisateur(
                nom="Garcia",
                prenom="Ana",
                email="ana.garcia@example.com",
                mot_de_passe=hash_password("client123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=client_role.id
            ),
            Utilisateur(
                nom="Leroy",
                prenom="Thomas",
                email="thomas.leroy@example.com",
                mot_de_passe=hash_password("client123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=client_role.id
            ),
            Utilisateur(
                nom="Moreau",
                prenom="Julie",
                email="julie.moreau@example.com",
                mot_de_passe=hash_password("client123"),  # Utilisation de bcrypt
                status="ACTIVE",
                role_id=client_role.id
            )
        ]

        for utilisateur in utilisateurs:
            db.session.add(utilisateur)

        db.session.commit()

    # Vérifier si les manageurs existent déjà
    if Manageur.query.count() == 0:
        # Récupérer les utilisateurs manageurs
        marie = Utilisateur.query.filter_by(email="marie.dupont@example.com").first()
        pierre = Utilisateur.query.filter_by(email="pierre.martin@example.com").first()

        # Création des manageurs
        manageurs = [
            Manageur(utilisateur_id=marie.id),
            Manageur(utilisateur_id=pierre.id)
        ]

        for manageur in manageurs:
            db.session.add(manageur)

        db.session.commit()

    # Vérifier si les livreurs existent déjà
    if Livreur.query.count() == 0:

        # Récupérer les utilisateurs livreurs et manageurs
        luc = Utilisateur.query.filter_by(email="luc.bernard@example.com").first()
        sophie = Utilisateur.query.filter_by(email="sophie.petit@example.com").first()
        jean = Utilisateur.query.filter_by(email="jean.robert@example.com").first()
        marie_manager = Manageur.query.filter_by(
            utilisateur_id=Utilisateur.query.filter_by(email="marie.dupont@example.com").first().id).first()
        pierre_manager = Manageur.query.filter_by(
            utilisateur_id=Utilisateur.query.filter_by(email="pierre.martin@example.com").first().id).first()

        # Création des livreurs
        livreurs = [
            Livreur(utilisateur_id=luc.id, manageur_id=marie_manager.id),
            Livreur(utilisateur_id=sophie.id, manageur_id=marie_manager.id),
            Livreur(utilisateur_id=jean.id, manageur_id=pierre_manager.id)
        ]

        for livreur in livreurs:
            db.session.add(livreur)

        db.session.commit()

    # Vérifier si les clients existent déjà
    if Client.query.count() == 0:
        print("Création des clients...")

        # Récupérer les utilisateurs clients
        ana = Utilisateur.query.filter_by(email="ana.garcia@example.com").first()
        thomas = Utilisateur.query.filter_by(email="thomas.leroy@example.com").first()
        julie = Utilisateur.query.filter_by(email="julie.moreau@example.com").first()

        # Création des clients
        clients = [
            Client(utilisateur_id=ana.id, lieu_livraison="123 Avenue des Champs, Paris"),
            Client(utilisateur_id=thomas.id, lieu_livraison="45 Rue de la Paix, Lyon"),
            Client(utilisateur_id=julie.id, lieu_livraison="78 Boulevard Saint-Michel, Marseille")
        ]

        for client in clients:
            db.session.add(client)

        db.session.commit()