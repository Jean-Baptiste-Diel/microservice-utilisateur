from sqlalchemy.exc import SQLAlchemyError

from models import Manageur, Livreur
from utils.fonction import *

def creation_livreur(manageur_id, donnees):
    """
    Creation d'une livreur par un manageur
    :param manageur_id:
    :param donnees:
    :return: reponse en format json
    """
    try:
        if not db.session.is_active:
            db.session.begin()
        mot_de_passe_hasher = preparation_des_donnees(donnees)
        if isinstance(mot_de_passe_hasher, tuple):
            # preparation_des_donnees a renvoyé une réponse d'erreur
            return mot_de_passe_hasher
        # Vérification que le manageur existe
        manageur = Manageur.query.filter_by(utilisateur_id=manageur_id).first()
        print(manageur)
        if not manageur:
            return jsonify({"error": "Manageur spécifié introuvable"}), 404
        # Création dans une transaction
        with db.session():
            # Creation de l'utilisateur
            nouvel_utilisateur = Utilisateur(
                nom=donnees['nom'],
                prenom=donnees['prenom'],
                email=donnees['email'],
                mot_de_passe=mot_de_passe_hasher,
                role_id=4,
            )
            db.session.add(nouvel_utilisateur)
            db.session.flush()
            # Creation du livreur
            livreur = Livreur(utilisateur_id=nouvel_utilisateur.id, manageur_id=manageur.id)
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
            "details": str(e)}), 500

def info_livreur(livreur_id):
    """
    Récupère les informations d'un livreur par son ID
    Le token JWT doit être fourni dans le header Authorization
    """
    try:
        # Rechercher l'utilisateur
        livreur = Livreur.query.filter_by(id=livreur_id).first()
        if not livreur:
            return jsonify({"message": "Utilisateur introuvable"}), 404

        # Construire la réponse
        utilisateur = livreur.utilisateur
        if not utilisateur:
            return jsonify({"message": "Utilisateur introuvable pour ce client"}), 404

        response = {
            "id": utilisateur.id,
            "email": utilisateur.email,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "role": utilisateur.role.nom_du_role,
            "livreur_id": livreur.id,
        }

        print(f"Utilisateur trouvé : {response}")
        return jsonify(response), 200

    except Exception as e:
        print("Erreur :", e)
        return jsonify({"message": "Erreur lors de la récupération de l'utilisateur"}), 500
