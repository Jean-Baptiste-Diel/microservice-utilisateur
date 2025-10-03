from flask import Blueprint, request, jsonify, json
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity

from services.crud.crud_livraison import ajouter_livraison, afficher_livraison

livraison_bp = Blueprint('livraison_bp', __name__)

@livraison_bp.route('/creer-livraison', methods=['POST'])
def creer_livraison_route():
    creer_livraison = ajouter_livraison()
    return creer_livraison

@livraison_bp.route('/livraison', methods=['GET'])
@jwt_required()
def afficher_livraison_route():
    auth_header = request.headers.get("Authorization")
    print("🔑 Header Authorization reçu :", auth_header)

    if not auth_header:
        return jsonify({"message": "Header Authorization manquant"}), 401
    try:
        verify_jwt_in_request()
        user_str = get_jwt_identity()  # Transforme en dict
        print(user_str)
        user = json.loads(user_str)
        print("📝 Payload JWT :", user)

        if user.get("role") != "Client" and user.get("role") != "Livreur":
            return jsonify({"error": "Action non autorisée"}), 403

        client_id = user.get("client_id")
        livreur_id = user.get("livreur_id")
        if client_id:
            livraisons = afficher_livraison(client_id=client_id)
            return livraisons
        if livreur_id:
            livraisons = afficher_livraison(livreur_id=livreur_id)
            return livraisons
    except Exception as e:
        print("❌ Erreur :", e)
        return jsonify({"message": "Erreur serveur", "details": str(e)}), 500