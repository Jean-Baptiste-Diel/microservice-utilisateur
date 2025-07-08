from http.client import responses

import bcrypt
from flask import jsonify, request, session
from sqlalchemy.exc import SQLAlchemyError

from configs.config import db
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

        if bcrypt.checkpw( donnees['mot_de_passe'].encode('utf-8'), utilisateur.mot_de_passe.encode('utf-8')):
            response ={"message": "Identifiant valide",
                            "utilisateur":{
                                "id": utilisateur.id,
                                "email": utilisateur.email,
                            }
                        }
            return jsonify(response), 200
        else:
            return jsonify({"message": "Identifiant invalide"}), 401
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Erreur de base de données"}), 500
    except Exception as e:
        return jsonify({"message": "Erreur serveur"}), 500


def deconnexion():
    session.clear()
    return jsonify({"message": "Déconnexion réussie"}), 200