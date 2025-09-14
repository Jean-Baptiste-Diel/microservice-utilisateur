import re
from typing import Tuple, Optional
import bcrypt
from flask import jsonify

from configs.config import db
from models import Utilisateur, Role

def validation_email(email: str, utilisateur_id: int = None) -> Tuple[Optional[dict], Optional[int]]:
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return {"message": "Format d'email invalide"}, 400
    # Vérification email unique
        # 2. Vérification unicité (sauf pour l'utilisateur actuel si spécifié)
    query = Utilisateur.query.filter_by(email=email)
    if utilisateur_id is not None:
        query = query.filter(Utilisateur.id != utilisateur_id)
    if query.first():
        return {"message": "Cet email est déjà utilisé"}, 409
        # 3. Succès
    return None, None

def validation_des_maj_utilisateur(donnees, utilisateur):
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
                    return jsonify({"message": "Format d'email invalide"}), 400
                if Utilisateur.query.filter(Utilisateur.email == donnees['email'],
                                            Utilisateur.id != utilisateur.id).first():
                    return jsonify({"message": "Cet email est déjà utilisé par un autre utilisateur"}), 409

            # Validation spéciale pour le rôle
            elif champ == 'role_id':
                if not Role.query.get(donnees['role_id']):
                    return jsonify({"message": "Rôle spécifié introuvable"}), 404

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
    return None

def preparation_des_donnees(donnees):
    # Validation des données
    if not donnees:
        return jsonify({"error": "Aucune donnée fournie"}), 400
    champs_requis = ['nom', 'prenom', 'email', 'mot_de_passe']
    if not all(champ in donnees for champ in champs_requis):
        print(donnees)
        return jsonify({
            "message": "Champs manquants",
            "requis": champs_requis,
            "reçus": list(donnees.keys())
        }), 400
    # Validation email
    message_erreur, code_erreur = validation_email(donnees['email'])
    if message_erreur:
        return jsonify(message_erreur), code_erreur
    # Vérification rôle existe
    #role = db.session.get(Role, donnees['role_id'])
    #if not role:
    #    return jsonify({"message": "Rôle spécifié introuvable"}), 404
    # Hachage mot de passe
    mot_de_passe_hasher = bcrypt.hashpw(
        donnees['mot_de_passe'].encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    return mot_de_passe_hasher