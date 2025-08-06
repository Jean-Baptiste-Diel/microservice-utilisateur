import re
import bcrypt
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from configs.config import db
from models import Manageur, Utilisateur, Role, Livreur
from utils import fonction
from utils.fonction import validation_email, validation_des_maj_utilisateur


def creation_livreur(manageur_id, donnees):
    try:
        if not all(champ in donnees for champ in ['nom', 'prenom', 'email', 'mot_de_passe']):
            return jsonify({"error": "Champs manquants"}), 400
        # Validation email
        validation_email(donnees['email'])
        # Vérification rôle existe
        #role = Role.query.get(donnees['role_id'])
        role = db.session.get(Role, donnees['role_id'])
        if not role:
            return jsonify({"error": "Rôle spécifié introuvable"}), 404
        # Vérification que le manageur existe
        manageur = db.session.get(Manageur, manageur_id)
        if not manageur:
            return jsonify({"error": "Manageur spécifié introuvable"}), 404
        # Hachage mot de passe
        mot_de_passe_hasher = bcrypt.hashpw(
            donnees['mot_de_passe'].encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        # Création dans une transaction
        with db.session():
            # Creation de l'utilisateur
            nouvel_utilisateur = Utilisateur(
                nom=donnees['nom'],
                prenom=donnees['prenom'],
                email=donnees['email'],
                mot_de_passe=mot_de_passe_hasher,
                role_id=donnees['role_id'],
                status="ACTIVE"  # Ajout du statut par défaut
            )
            db.session.add(nouvel_utilisateur)
            db.session.flush()  # Pour obtenir l'ID
            # Creation du livreur
            livreur = Livreur(
                utilisateur_id=nouvel_utilisateur.id,
                manageur_id=manageur.id
            )
            db.session.add(livreur)
            db.session.commit()

            reponse = {
                "message": "Livreur créé avec succès",
                "livreur": {
                    "id": livreur.id,
                    "utilisateur_id": nouvel_utilisateur.id,
                    "manageur_id": manageur.id
                }
            }
        return jsonify(reponse), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Erreur de base de données",
            "details": str(e)
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Erreur serveur inattendue",
            "details": str(e)
        }), 500

def mettre_a_jour_livreur(livreur_id):
    try:
        donnees = request.get_json()

        # Validation de base
        if not donnees:
            return jsonify({"error": "Aucune donnée fournie"}), 400

        # Récupération du livreur
        livreur = Livreur.query.get(livreur_id)
        if not livreur:
            return jsonify({"error": "Livreur non trouvé"}), 404

        utilisateur = livreur.utilisateur

        validation_des_maj_utilisateur(donnees, utilisateur)

        db.session.commit()
        return jsonify({
            "message": "Livreur mis à jour avec succès",
            "livreur_id": livreur.id,
            "utilisateur_id": utilisateur.id,
            "manageur_id": livreur.manageur_id
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Erreur de base de données",
            "details": str(e)
        }), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Erreur serveur inattendue",
            "details": str(e)
        }), 500