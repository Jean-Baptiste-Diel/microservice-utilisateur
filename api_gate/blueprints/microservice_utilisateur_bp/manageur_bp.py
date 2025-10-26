from flask import Blueprint, request, jsonify
import requests

livreurs_bp = Blueprint("livreurs_bp", __name__)
URL_SERVICE_MANAGEUR = "http://localhost:5000"  # ton microservice manageur

@livreurs_bp.route("/livreurs", methods=["GET"])
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
            "message": "Erreur de communication avec le microservice manageur",
            "details": str(e)
        }), 500
