from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from configs.config import db
from models import Livraison

def ajouter_livraison():
    try:
        donnees = request.get_json()
        champs_requis = ['client_id', 'livreur_id']
        if not all(champ in donnees for champ in champs_requis):
            return jsonify({'error': 'Tous les champs sont requis'}), 400

        def generateur_matricule():
            matricule = "7"
            return matricule

        nouvel_livraison = Livraison(
            matricule=generateur_matricule(),
            livreur_id=donnees['livreur_id'],
            client_id=donnees['client_id'],
        )
        db.session.add(nouvel_livraison)
        db.session.commit()
        return jsonify({"message": "livraison ajouter"}),201
    except SQLAlchemyError as e:
        return jsonify({'erreur': str(e)}), 500

def afficher_livraison(client_id):
    try:
        livraisons = Livraison.query.filter_by(client_id=client_id).all()
        print(livraisons)
        return jsonify([livraison.to_dict() for livraison in livraisons]), 200
    except SQLAlchemyError as e:
        return jsonify({'erreur': str(e)}), 400