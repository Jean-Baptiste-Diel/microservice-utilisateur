# python
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.service_statistique import *

statistique_bp = Blueprint("statistique_bp", __name__, url_prefix="/")

@statistique_bp.route("livreurs/<int:livreur_id>/stats", methods=["GET"])
@jwt_required(optional=True)
def stats_livreur(livreur_id: int):
    data = recuperer_statistiques_pour_livreur(livreur_id)
    if not data:
        return jsonify({"message": "Aucune statistique disponible pour ce livreur."}), 404
    return jsonify(data), 200

@statistique_bp.route("stats/recompute", methods=["POST"])
@jwt_required()  # protéger cette route
def recompute_all():
    recalculer_toutes_les_statistiques()
    return jsonify({"message": "Recalcul des statistiques terminé."}), 200

@statistique_bp.route("livreurs/<int:livreur_id>/stats/recompute", methods=["POST"])
@jwt_required()  # protéger cette route
def recompute_one(livreur_id: int):
    recalculer_statistiques_pour_livreur(livreur_id)
    return jsonify({"message": "Statistiques recalculées pour le livreur.", "livreur_id": livreur_id}), 200