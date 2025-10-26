import json

from flask import blueprints, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.crud.crud_client import info_client

livreur_bp = blueprints.Blueprint('livreur_bp', __name__)

@livreur_bp.route('/client/<int:client_id>', methods=['GET'])
@jwt_required()
def get_utilisateur(client_id):
    """
    Récupère les informations d'un utilisateur par son ID
    Le token JWT doit être fourni dans le header Authorization pour verifier le role
    pour recuper les information client et l'afficher chez le livreur
    """
    try:
        # Récupérer l'identité depuis le token
        identity = get_jwt_identity()
        user = json.loads(identity)
        if user.get("role") != "Livreur":
            return jsonify({"error": "Action non autorisée"}), 403
        information_client = info_client(client_id)
        return information_client

    except Exception as e:
        print("Erreur :", e)
        return jsonify({"message": "Erreur lors de la récupération de l'utilisateur"}), 500