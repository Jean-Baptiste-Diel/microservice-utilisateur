import bcrypt
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from configs.config import db
from models import Utilisateur, Role
from utils.fonction import preparation_des_donnees


def creation_utilisateur():
    try:
        donnees = request.get_json()
        # Validation des champs
        mot_de_passe_hasher = preparation_des_donnees(donnees)
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
        return jsonify({
            "message": "Erreur de base de données",
            "details": e}), 500

def archiver_utilisateur(id_utilisateur):
    try:
        utilisateur = Utilisateur.query.get(id_utilisateur)
        if not utilisateur:
            return jsonify({"message": "Utilisateur introuvable"}), 404
        utilisateur.status = "INACTIVE"
        db.session.commit()
        return jsonify({"message": "Utilisateur archivé avec succès"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "message": "Erreur de base de données",
            "details": e}), 500

def mettre_a_jour_utilisateur(id_utilisateur: int | None = None, client_id: int | None = None, livreur_id: int | None = None, manageur_id: int | None = None):
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
        return jsonify({
            "message": "Erreur de base de données",
            "error": e}), 500