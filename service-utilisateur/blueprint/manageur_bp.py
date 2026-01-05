import json

from flask import Blueprint, jsonify, request
from flask_jwt_extended import verify_jwt_in_request,jwt_required, get_jwt, get_jwt_identity

from services.crud.crud_livreur import creation_livreur
from services.crud.crud_manageur import creation_manageur
from services.service_manageur import afficher_livreurs, afficher_livreur, rechercher_livreur, bloquer_livreur, \
    afficher_livreurs1

manageur_bp = Blueprint('manageur_bp', __name__)

erreur = "Erreur serveur"
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

@manageur_bp.route('/creation-livreur', methods=["POST"])
@jwt_required()
def creation_livreur_route():
    auth_header = request.headers.get("Authorization")
    print("🔑 Header Authorization reçu :", auth_header)

    if not auth_header:
        return jsonify({"message": "Header Authorization manquant"}), 401
    try:
        verify_jwt_in_request()  # Vérifie la présence et validité du token
        identity_str = get_jwt_identity()  # Récupère la string
        user = json.loads(identity_str)  # Transforme en dict
        if user.get("role") != "Manageur":
            return jsonify({"error": "Action non autorisée"}), 403

        manageur_id = user.get("id")
        # 2. Passe la main à la fonction de service
        print("manageur_id = ", manageur_id)
        donnees = request.get_json()
        print("Donnees = ", donnees)

        return creation_livreur(manageur_id, donnees)
    except Exception as e:
        return jsonify({"message": erreur,
                        "details": e}), 500

@manageur_bp.route('/livreurs1', methods=["GET"])
def afficher_all_livreurs():
    return afficher_livreurs1()
@manageur_bp.route('/livreurs', methods=["GET"])
@jwt_required()
def afficher_livreurs_route():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"message": "Header Authorization manquant"}), 401
    try:
        verify_jwt_in_request()  # Vérifie la présence et validité du token
        identity_str = get_jwt_identity()  # Récupère la string
        user = json.loads(identity_str)
        if user.get("role") != "Manageur":
            return jsonify({"error": "Action non autorisée"}), 403

        manageur_id = user.get("id")
        # NE PAS FAIRE jsonify si afficher_livreurs renvoie déjà un Response
        return afficher_livreurs(manageur_id)
    except Exception as e:
        print("❌ Erreur :", e)
        return jsonify({"message": erreur,
                        "details": str(e)}), 500


@manageur_bp.route('/livreur', methods=["GET"])
@jwt_required()
def afficher_livreur_route():
    auth_header = request.headers.get("Authorization")
    print("🔑 Header Authorization reçu :", auth_header)

    if not auth_header:
        return jsonify({"message": "Header Authorization manquant"}), 401
    try:
        verify_jwt_in_request()  # Vérifie la présence et validité du token
        identity_str = get_jwt_identity()  # Récupère la string
        user = json.loads(identity_str)

        if user.get("role") != "Manageur":
            return jsonify({"error": "Action non autorisée"}), 403

        livreur_id = user.get("livreur_id")
        manageur_id = user.get("id")
        return afficher_livreur(livreur_id)
    except Exception as e:
        return jsonify({"message": erreur,
                        "details": e}), 500

@manageur_bp.route('/research', methods=["GET"])
@jwt_required()
def search_livreur_route(manageur_id):
    try:
        claims = get_jwt()
        if claims.get('role') != 'Manageur' or claims.get('user_id') != manageur_id:
            return jsonify({"error": "Action non autorisée"}), 403
        terme = request.args.get("q", "")
        return rechercher_livreur(terme)
    except Exception as e:
        return jsonify({"message": erreur,
                        "details": e}), 500

@manageur_bp.route('/bloquer/<int:livreur_id>', methods=["PATCH"])
@jwt_required()
def bloquer_route(livreur_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"message": "Header Authorization manquant"}), 401
    try:
        verify_jwt_in_request()
        identity_str = get_jwt_identity()
        user = json.loads(identity_str)
        if user.get("role") != "Manageur":
            return jsonify({"error": "Action non autorisée"}), 403
        bloquer = bloquer_livreur(livreur_id)
        return bloquer
    except Exception as e:
        return jsonify({"message": "Erreur serveur",
                        "details": e}), 500