from flask import request
from sqlalchemy.exc import SQLAlchemyError
from models import Client
from utils.fonction import *

def creation_client():
    try:
        if not db.session.is_active:
            db.session.begin()
        donnees = request.get_json()
        # 2) Validation / préparation générique
        mot_de_passe_hasher = preparation_des_donnees(donnees)
        if isinstance(mot_de_passe_hasher, tuple):
            # preparation_des_donnees a renvoyé une réponse d'erreur
            return mot_de_passe_hasher
        # Création dans une transaction
        with db.session():
            # Creation de l'utilisateur
            nouvel_utilisateur = Utilisateur(
                nom=donnees['nom'],
                prenom=donnees['prenom'],
                email=donnees['email'],
                mot_de_passe=mot_de_passe_hasher,
                role_id=donnees['role_id'],
            )
            db.session.add(nouvel_utilisateur)
            # Creation du manageur
            db.session.flush()  # Pour obtenir l'ID
            client = Client(utilisateur_id=nouvel_utilisateur.id, lieu_livraison = donnees['adresse'])
            db.session.add(client)
            db.session.commit()
            reponse = {
                "message": "Client créé avec succès",
                "client": {
                    "id": client.id,
                    "utilisateur_id": nouvel_utilisateur.id
                }
            }
            return jsonify(reponse), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "message": "Erreur de base de données",
            "details": str(e)}), 500

def info_client(client_id):
    """
    Récupère les informations d'un client par son ID
    Le token JWT doit être fourni dans le header Authorization
    """
    try:
        # Rechercher l'utilisateur
        client = Client.query.filter_by(id=client_id).first()
        if not client:
            return jsonify({"message": "Utilisateur introuvable"}), 404

        # Construire la réponse
        utilisateur = client.utilisateur
        if not utilisateur:
            return jsonify({"message": "Utilisateur introuvable pour ce client"}), 404

        response = {
            "id": utilisateur.id,
            "email": utilisateur.email,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "role": utilisateur.role.nom_du_role,
            "client_id": client.id,
        }

        print(f"Utilisateur trouvé : {response}")
        return jsonify(response), 200

    except Exception as e:
        print("Erreur :", e)
        return jsonify({"message": "Erreur lors de la récupération de l'utilisateur"}), 500
