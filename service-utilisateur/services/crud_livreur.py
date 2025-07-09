import re
import bcrypt
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from configs.config import db
from models import Manageur, Utilisateur, Role, Livreur


def creation_livreur(manageur_id):
    try:
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
        #role = Role.query.get(donnees['role_id'])
        role = db.session.get(Role, donnees['role_id'])
        if not role:
            return jsonify({"error": "Rôle spécifié introuvable"}), 404

        # Vérification que le manageur existe
        #manageur = Manageur.query.get(manageur_id)
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
                    donnees['mot_de_passe'] = bcrypt.hashpw(
                        donnees['mot_de_passe'].encode('utf-8'),
                        bcrypt.gensalt()
                    ).decode('utf-8')

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