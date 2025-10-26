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

def afficher_livraison(client_id=None, livreur_id=None, manageur_id=None):
    try:
        result = []
        # Filtrage selon le type d’utilisateur
        if client_id:
            livraisons = Livraison.query.filter_by(client_id=client_id).all()
        elif livreur_id:
            livraisons = Livraison.query.filter_by(livreur_id=livreur_id).all()
        elif manageur_id:
            livraisons = Livraison.query.all()
        else:
            return jsonify({'error': 'Aucun identifiant fourni'}), 400
        # Construction du résultat
        for livraison in livraisons:
            data = livraison.to_dict()
            result.append(data)
            # Debug
            print(f"📦 Livraison récupérée : {data}")
        print(f"✅ Total livraisons trouvées : {len(result)}")
        return jsonify(result), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print("❌ Erreur SQLAlchemy :", str(e))
        return jsonify({'erreur': str(e)}), 400
