
import bcrypt
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from configs.config import db
from models import Utilisateur, Role
from utils.fonction import validation_email


def creation_utilisateur():
    try:
        donnees = request.get_json()
        # Validation des champs
        champs_requis = ['nom', 'prenom', 'email', 'mot_de_passe', 'role_id']
        if not all(champ in donnees for champ in champs_requis):
            return jsonify({"error": "Champs manquants", "requis": champs_requis}), 400
        # Validation email
        validation_email(donnees['email'])
        # Vérification rôle existe
        role = db.session.get(Role, donnees['role_id'])
        if not role:
            return jsonify({"error": "Rôle spécifié introuvable"}), 404
        # Hachage mot de passe
        mot_de_passe_hasher = bcrypt.hashpw(donnees['mot_de_passe'].encode('utf-8'), bcrypt.gensalt())
        # Création utilisateur
        nouvel_utilisateur = Utilisateur(
            nom=donnees['nom'],
            prenom=donnees['prenom'],
            email=donnees['email'],
            mot_de_passe=mot_de_passe_hasher.decode('utf-8'),
            role_id=donnees['role_id']
        )
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        return jsonify({
            "id": nouvel_utilisateur.id,
            "nom": nouvel_utilisateur.nom,
            "prenom": nouvel_utilisateur.prenom,
            "email": nouvel_utilisateur.email,
            "role_id": nouvel_utilisateur.role_id
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Erreur de base de données"}), 500
    except Exception as e:
        return jsonify({"error": "Erreur serveur"}), 500

def archiver_utilisateur(id_utilisateur):
    try:
        utilisateur = Utilisateur.query.get(id_utilisateur)
        if not utilisateur:
            return jsonify({"error": "Utilisateur introuvable"}), 404
        utilisateur.status = "archive"
        db.session.commit()
        return jsonify({"message": "Utilisateur archivé avec succès"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Erreur de base de données"}), 500

def mettre_a_jour_utilisateur(id_utilisateur: None, client_id: None, livreur_id: None, manageur_id: None):
    try:
        utilisateur = Utilisateur.query.get(id_utilisateur)
        if not utilisateur:
            return jsonify({"error": "Utilisateur introuvable"}), 404
        donnees = request.get_json()
        # Mise à jour des champs
        if 'nom' in donnees:
            utilisateur.nom = donnees['nom']
        if 'prenom' in donnees:
            utilisateur.prenom = donnees['prenom']
        if 'email' in donnees:
            # Vérification nouvel email
            if donnees['email'] != utilisateur.email:
                if Utilisateur.query.filter_by(email=donnees['email']).first():
                    return jsonify({"error": "Email déjà utilisé"}), 409
                utilisateur.email = donnees['email']
        if 'mot_de_passe' in donnees:
            mot_de_passe_hasher = bcrypt.hashpw(donnees['mot_de_passe'].encode('utf-8'), bcrypt.gensalt())
            utilisateur.mot_de_passe = mot_de_passe_hasher.decode('utf-8')
        if 'role_id' in donnees:
            if not Role.query.get(donnees['role_id']):
                return jsonify({"error": "Rôle introuvable"}), 404
            utilisateur.role_id = donnees['role_id']
        db.session.commit()
        return jsonify({"message": "Utilisateur mis à jour avec succès"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Erreur de base de données"}), 500