import json

import bcrypt
from flask import jsonify, request, session
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError
from models import Utilisateur

def connexion():
    try:
        donnees = request.get_json()
        if not donnees:
            return jsonify({"message": "Tous les champs sont requis"}), 400
        champs_requis = ['email', 'mot_de_passe']
        if not all(champ in donnees for champ in champs_requis):
            return jsonify({"message": "Tous les champs sont requis"}), 400
        utilisateur = Utilisateur.query.filter_by(email=donnees["email"]).first()
        if not utilisateur:
            return jsonify({"message": "Identifiant invalide"}), 401
        if bcrypt.checkpw(donnees['mot_de_passe'].encode('utf-8'),
                          utilisateur.mot_de_passe.encode('utf-8')):
            # ✅ Créer le token JWT
            payload = {
                "id": utilisateur.id,
                "email": utilisateur.email,
                "role": utilisateur.role.nom_du_role
            }
            # 🔥 Si c’est un client, ajouter ses infos Client
            if utilisateur.role.nom_du_role == "Client" and utilisateur.client:
                payload["client_id"] = utilisateur.client.id
                payload["nom"] = utilisateur.nom
                payload["prenom"] = utilisateur.prenom
                payload["lieu_livraison"] = utilisateur.client.lieu_livraison
            # 🔥 Si c’est un manageur, ajouter ses infos Manageur
            if utilisateur.role.nom_du_role == "Manageur" and utilisateur.manageur:
                payload["manageur_id"] = utilisateur.manageur.id

            # 🔥 Ajout si Livreur
            if utilisateur.role.nom_du_role == "Livreur" and utilisateur.livreur:
                payload["livreur_id"] = utilisateur.livreur.id
                payload["manageur_id"] = utilisateur.livreur.manageur_id

            access_token = create_access_token(identity=json.dumps(payload))

            # ✅ Réponse plus claire
            response = {
                "message": "Identifiant valide",
                "access_token": access_token,
                "utilisateur": {
                    "id": utilisateur.id,
                    "email": utilisateur.email,
                    "role": utilisateur.role.nom_du_role,
                    "nom": utilisateur.nom,
                    "prenom": utilisateur.prenom,
                    # si client : infos supplémentaires
                    **({"client_id": utilisateur.client.id, "utilisateur_id": utilisateur.client.utilisateur_id,
                        "lieu_livraison": utilisateur.client.lieu_livraison} if utilisateur.role.nom_du_role == "Client" and utilisateur.client else {}),
                    # si manageur : infos supplémentaires
                    **({
                           "manageur_id": utilisateur.manageur.id} if utilisateur.role.nom_du_role == "Manageur" and utilisateur.manageur else {}),
                    # si livreur : infos supplémentaires
                    **({"livreur_id": utilisateur.livreur.id,
                        "manageur_id": utilisateur.livreur.manageur_id} if utilisateur.role.nom_du_role == "Livreur" and utilisateur.livreur else {})
                }
            }
            return jsonify(response), 200

        return jsonify({"message": "Identifiant invalide"}), 401

    except SQLAlchemyError as e:
        print(e)
        return jsonify({"message": "Erreur de base de données"}), 500

def deconnexion():
    session.clear()
    return jsonify({"message": "Déconnexion réussie"}), 200