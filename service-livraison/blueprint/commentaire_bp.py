

from flask import Blueprint, jsonify, request, json
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from services.crud import crud_commentaire
commentaire_bp = Blueprint('commentaire', __name__)
@commentaire_bp.route('/ajouter-commentaire', methods=['POST'])
def ajouter_commentaire_route():
    auth_header = request.headers.get("Authorization")
    # print("🔑 Header Authorization reçu :", auth_header)
    if not auth_header:
        return jsonify({"message": "Header Authorization manquant"}), 401
    try:
        verify_jwt_in_request()
        user_str = get_jwt_identity()
        user = json.loads(user_str)
        # print("📝 Payload JWT :", user)
        if user.get("role") != "Client":
            return jsonify({"error": "Action non autorisée"}), 403

        commentaire = crud_commentaire.ajouter_commentaire()
        return commentaire
    except Exception as e:
        print("❌ Erreur :", e)
        return jsonify({"message": "Erreur serveur", "details": str(e)}), 500

@commentaire_bp.route('/modifier-commentaire/<int:id>', methods=['PUT'])
def modifier_commentaire_route(id):
    auth_header = request.headers.get("Authorization")
    # print("🔑 Header Authorization reçu :", auth_header)
    if not auth_header:
        return jsonify({"message": "Header Authorization manquant"}), 401
    try:
        verify_jwt_in_request()
        user_str = get_jwt_identity()
        user = json.loads(user_str)
        # print("📝 Payload JWT :", user)
        if user.get("role") != "Client":
            return jsonify({"error": "Action non autorisée"}), 403
        commentaire = crud_commentaire.modifier_commentaire(id)
        return commentaire
    except Exception as e:
        print("❌ Erreur :", e)
        return jsonify({"message": "Erreur serveur", "details": str(e)}), 500
@commentaire_bp.route('/supprimer/<int:id>', methods=['POST'])
def supprimer_commentaire_route(id):
    supprimer = crud_commentaire.archiver_commentaire(id)
    return supprimer