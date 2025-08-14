from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from services.crud.crud_livreur import creation_livreur
from services.crud.crud_manageur import creation_manageur

manageur_bp = Blueprint('manageur_bp', __name__)

@manageur_bp.route('/creation-manageur', methods=["POST"])
@jwt_required()
def creation_manageur_route():
    try:
        claims = get_jwt()
        if claims.get('role') != 'Manageur' :
            return jsonify({"error": "Action non autorisée"}), 403
        creation_utilisateur_mangeur = creation_manageur()
        return creation_utilisateur_mangeur
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@manageur_bp.route('/creation-livreur/<int:manageur_id>', methods=["POST"])
@jwt_required()
def creation_livreur_route(manageur_id):
    try:
        # 1. Vérification JWT et permissions
        claims = get_jwt()
        if claims.get('role') != 'Manageur' or claims.get('user_id') != manageur_id:
            return jsonify({"error": "Action non autorisée"}), 403
        # 2. Passe la main à la fonction de service
        return creation_livreur(manageur_id, request.get_json())
    except Exception as e:
        return jsonify({"message": "Erreur serveur",
                        "details": e}), 500