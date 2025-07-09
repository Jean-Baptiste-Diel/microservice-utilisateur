
from configs.config import db
from models import Manageur, Utilisateur, Role
from flask import jsonify, request
import re
import bcrypt
from sqlalchemy.exc import SQLAlchemyError

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
                "error": "Champs manquants",
                "requis": champs_requis,
                "reçus": list(donnees.keys())
            }), 400

        # Validation email
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", donnees['email']):
            return jsonify({"error": "Format d'email invalide"}), 400

        # Vérification email unique
        if Utilisateur.query.filter_by(email=donnees['email']).first():
            return jsonify({"error": "Cet email est déjà utilisé"}), 409

        # Vérification rôle existe
        role = db.session.get(Role, donnees['role_id'])
        if not role:
            return jsonify({"error": "Rôle spécifié introuvable"}), 404

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
            "error": "Erreur de base de données",
            "details": str(e)
        }), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Erreur serveur inattendue",
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

        # Champs autorisés pour mise à jour
        champs_modifiables = {
            'nom': str,
            'prenom': str,
            'email': str,
            'mot_de_passe': str,
            'status': str,
            'role_id': int
        }

        # Validation et traitement des champs
        for champ, type_donnee in champs_modifiables.items():
            if champ in donnees:
                # Validation spéciale pour l'email
                if champ == 'email':
                    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", donnees['email']):
                        return jsonify({"error": "Format d'email invalide"}), 400
                    if Utilisateur.query.filter(Utilisateur.email == donnees['email'],
                                                Utilisateur.id != utilisateur.id).first():
                        return jsonify({"error": "Cet email est déjà utilisé par un autre utilisateur"}), 409

                # Validation spéciale pour le rôle
                elif champ == 'role_id':
                    if not Role.query.get(donnees['role_id']):
                        return jsonify({"error": "Rôle spécifié introuvable"}), 404

                # Validation spéciale pour le mot de passe
                elif champ == 'mot_de_passe':
                    if len(donnees['mot_de_passe']) < 8:
                        return jsonify({"error": "Le mot de passe doit contenir au moins 8 caractères"}), 400
                    donnees['mot_de_passe'] = bcrypt.hashpw(donnees['mot_de_passe'].encode('utf-8'),
                                                            bcrypt.gensalt()).decode('utf-8')

                # Conversion du type de données
                try:
                    donnees[champ] = type_donnee(donnees[champ])
                except (ValueError, TypeError):
                    return jsonify({"error": f"Valeur invalide pour le champ {champ}"}), 400

                # Mise à jour de l'attribut
                setattr(utilisateur, champ, donnees[champ])

        # Validation du status
        if 'status' in donnees and donnees['status'] not in ['ACTIVE', 'INACTIVE', 'SUSPENDED']:
            return jsonify({"error": "Statut invalide"}), 400

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