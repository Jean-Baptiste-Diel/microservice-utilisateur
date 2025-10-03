from flask import Blueprint, jsonify
from configs.config import db
from models import Livraison, Commentaire, Statistique
from sqlalchemy import func
from datetime import datetime, timezone

statistique_bp = Blueprint("statistique_bp", __name__)

def mettre_a_jour_statistiques(livreur_id: int):
    # Compter les commentaires
    total = db.session.query(func.count(Commentaire.id)) \
        .join(Livraison) \
        .filter(Livraison.livreur_id == livreur_id) \
        .scalar() or 0

    bons = db.session.query(func.count(Commentaire.id)) \
        .join(Livraison) \
        .filter(Livraison.livreur_id == livreur_id, Commentaire.prediction == True) \
        .scalar() or 0

    mauvais = total - bons
    difference = bons - mauvais
    moyenne = bons / total if total > 0 else 0.0

    # Sauvegarder en base
    stat = Statistique.query.filter_by(livreur_id=livreur_id).first()
    if not stat:
        stat = Statistique(livreur_id=livreur_id)
        db.session.add(stat)

    stat.moyenne_evaluation = moyenne
    stat.nombre_commentaires = total
    stat.derniere_mise_a_jour = datetime.now(timezone.utc)
    db.session.commit()

    # Retourne toujours un dict utilisable par l’API
    return {
        "livreur_id": livreur_id,
        "moyenne_evaluation": moyenne,
        "nombre_commentaires": total,
        "bons": bons,
        "mauvais": mauvais,
        "difference": difference,
        "derniere_mise_a_jour": stat.derniere_mise_a_jour.isoformat()
    }

# 📌 Route : recalculer pour tous les livreurs
@statistique_bp.route("/statistiques/recalculer", methods=["POST"])
def recalculer_tous():
    livreurs = db.session.query(Livraison.livreur_id).distinct().all()
    resultats = []

    for (livreur_id,) in livreurs:
        stat_dict = mettre_a_jour_statistiques(livreur_id)  # dict et pas ORM
        resultats.append(stat_dict)

    return jsonify(resultats)

# 📌 Route : obtenir les stats d’un livreur
@statistique_bp.route("/statistiques/<int:livreur_id>", methods=["GET"])
def get_statistiques_livreur(livreur_id):
    stat_dict = mettre_a_jour_statistiques(livreur_id)
    return jsonify(stat_dict)
