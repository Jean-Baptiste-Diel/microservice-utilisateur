
from configs.config import db
from models import Manageur, Utilisateur, Role
from flask import jsonify, request
import re
import bcrypt
from sqlalchemy.exc import SQLAlchemyError

from utils.fonction import validation_email, validation_des_maj_utilisateur


def creation_manageur():
    try:
        if not db.session.is_active:
            db.session.begin()
        donnees = request.get_json()
        # Validation des données
        if not donnees:
            return jsonify({"error": "Aucune donnée fournie"}), 400

        champs_requis = ['nom', 'prenom', 'email', 'mot_de_passe', 'role_id']
        if not all(champ in donnees for champ in champs_requis):
            return jsonify({
                "message": "Champs manquants",
                "requis": champs_requis,
                "reçus": list(donnees.keys())
            }), 400

        # Validation email
        validation_email(donnees['email'])

        # Vérification rôle existe
        role = db.session.get(Role, donnees['role_id'])
        if not role:
            return jsonify({"message": "Rôle spécifié introuvable"}), 404

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
            )
            db.session.add(nouvel_utilisateur)
            # Creation du manageur
            db.session.flush()  # Pour obtenir l'ID
            manageur = Manageur(utilisateur_id=nouvel_utilisateur.id)
            db.session.add(manageur)
            db.session.commit()

            reponse = {
                "message": "Manager créé avec succès",
                "manageur": {
                    "id": manageur.id,
                    "utilisateur_id": nouvel_utilisateur.id
                }
            }
            return jsonify(reponse), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "message": "Erreur de base de données",
            "details": str(e)
        }), 500

def mettre_a_jour_manageur(manageur_id):
    try:
        donnees = request.get_json()

        # Validation de base
        if not donnees:
            return jsonify({"error": "Aucune donnée fournie"}), 400

        # Récupération du manager
        manageur = Manageur.query.get(manageur_id)
        if not manageur:
            return jsonify({"error": "Manager non trouvé"}), 404

        utilisateur = manageur.utilisateur

        validation_des_maj_utilisateur(donnees, utilisateur)

        db.session.commit()
        return jsonify({
            "message": "Manager mis à jour avec succès",
            "manageur_id": manageur.id,
            "utilisateur_id": utilisateur.id
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

def ajouter_livreur():
    pass

# Changer le statut du livreur
def mettre_a_jour_livreur():
    pass

def rechercher_livreur():
    pass

def statistiques():
    pass

def statistique_livreur(livreur_id):
    pass

def livraison_en_cours():
    pass

def rechercher_livraison():
    pass