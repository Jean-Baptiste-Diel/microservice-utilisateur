from sqlalchemy.exc import SQLAlchemyError
from models import Manageur, Livreur
from utils.fonction import *

def creation_livreur(manageur_id, donnees):
    try:
        if not db.session.is_active:
            db.session.begin()
        mot_de_passe_hasher = preparation_des_donnees(donnees)
        # Vérification que le manageur existe
        manageur = db.session.get(Manageur, manageur_id)
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
