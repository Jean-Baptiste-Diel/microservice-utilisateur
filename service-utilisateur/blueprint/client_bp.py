import json

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.crud.crud_client import creation_client
from services.crud.crud_livreur import info_livreur

client_bp = Blueprint('client', __name__)
erreur = "Erreur serveur"
@client_bp.route('/creer-client', methods=["POST"])
def creer_client_route():
    creer_client = creation_client()
    return creer_client

@client_bp.route('/livreur/<int:livreur_id>', methods=['GET'])
@jwt_required()
def get_utilisateur(livreur_id):
    """
    Récupère les informations d'un utilisateur par son ID
    Le token JWT doit être fourni dans le header Authorization pour verifier le role pour
    l'afficher chez le client
    """
    try:
        # Récupérer l'identité depuis le token
        identity = get_jwt_identity()
        user = json.loads(identity)
        if user.get("role") != "Client":
            return jsonify({"error": "Action non autorisée"}), 403
        information_livreur = info_livreur(livreur_id)
        return information_livreur

    except Exception as e:
        print("Erreur :", e)
        return jsonify({"message": "Erreur lors de la récupération de l'utilisateur"}), 500