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

            access_token = create_access_token(identity=json.dumps(payload))

            # ✅ Réponse plus claire
            response = {
                "message": "Identifiant valide",
                "access_token": access_token,  # <-- standard
                "utilisateur": {
                    "id": utilisateur.id,
                    "email": utilisateur.email,
                    "role": utilisateur.role.nom_du_role
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