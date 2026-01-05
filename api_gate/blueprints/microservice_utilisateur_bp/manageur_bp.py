from flask import Blueprint, request, jsonify
import requests

manageur_bp = Blueprint("manageur_bp", __name__)
URL_SERVICE_MANAGEUR = "http://localhost:5000"
message = "Erreur de communication avec le microservice utilisateur"
@manageur_bp.route("/livreurs", methods=["GET"])
def get_livreurs():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token manquant"}), 401
    try:
        # On transmet le JWT au microservice
        resp = requests.get(
            f"{URL_SERVICE_MANAGEUR}/livreurs",
            headers={"Authorization": token}
        )
        # Retourner la réponse telle quelle
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": message,
            "details": str(e)
        }), 500

@manageur_bp.route("/bloquer/<int:livreur_id>", methods=["PATCH"])
def bloquer_livreur_route(livreur_id):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token manquant"}), 401
    try:
        # On transmet le JWT au microservice
        resp = requests.patch(
            f"{URL_SERVICE_MANAGEUR}/bloquer/{livreur_id}",
            headers={"Authorization": token},
            json={}
        )
        # Retourner la réponse telle quelle
        return jsonify(resp.json()), resp.status_code,
    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": message,
            "details": str(e)
        }), 500