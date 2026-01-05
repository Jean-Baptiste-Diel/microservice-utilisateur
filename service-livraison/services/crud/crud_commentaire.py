# Python
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import join

from configs.config import db
from models import Commentaire, Livraison
from services.service_prediction import predict_sentiment


def ajouter_commentaire():
    donnees = request.get_json() or {}
    print(donnees)
    try:
        if not all(champs in donnees for champs in ['livraison_id', 'commentaire']):
            return jsonify({"error": "Champs manquants"}), 400
        # Prédire et forcer un booléen pour compatibilité JSON/DB
        prediction_val = bool(predict_sentiment(donnees['commentaire']))
        nouveau_commentaire = Commentaire(
            commentaire=donnees['commentaire'],
            prediction=prediction_val,
            livraison_id=donnees['livraison_id'],
        )
        db.session.add(nouveau_commentaire)
        db.session.commit()
        reponse = {
            "message": "Commentaire ajouté avec succès",
            "commentaire": {
                "id": nouveau_commentaire.id,
                "livraison_id": nouveau_commentaire.livraison_id,
                "prediction": nouveau_commentaire.prediction,
                "texte": nouveau_commentaire.commentaire
            },
        }
        return jsonify(reponse), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Erreur lors de l'ajout du commentaire",
            "details": str(e),
        }), 500

def modifier_commentaire(id):
    try:
        data = request.get_json()
        # 1️⃣ Récupérer le commentaire dans la base
        commentaire = Commentaire.query.get(id)
        if not commentaire:
            return jsonify({"message": "Commentaire introuvable"}), 404

        # 2️⃣ Mise à jour des champs
        commentaire.commentaire = data.get("commentaire", commentaire.commentaire)
        commentaire.prediction = data.get("prediction", commentaire.prediction)

        db.session.commit()

        # 3️⃣ Réponse avec le commentaire mis à jour
        return jsonify({
            "message": "Commentaire modifié avec succès",
            "commentaire": commentaire.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Erreur :", str(e))
        return jsonify({"error": str(e)}), 500

def archiver_commentaire(id):
    try:
        commentaire = Commentaire.query.get_or_404(id)
        commentaire.status = 'ARCHIVER'
        db.session.commit()
        return jsonify({'message': "Commentaire archivé avec succès"}), 200
    except SQLAlchemy as e:
        db.session.rollback()
        return jsonify({'message': "Erreur lors de l'archivage du commentaire",
                        'Details': f"{str(e)}"}), 500



