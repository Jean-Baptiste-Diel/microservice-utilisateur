from models import Manageur
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from utils.fonction import *

def creation_manageur():
    try:
        if not db.session.is_active:
            db.session.begin()

        donnees = request.get_json()
        mot_de_passe_hasher = preparation_des_donnees(donnees)
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
            "details": str(e)}), 500