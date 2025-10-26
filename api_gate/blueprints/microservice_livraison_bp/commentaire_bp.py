import requests
from flask import Blueprint, jsonify, request

URL_SERVICE_LIVRAISON = "http://localhost:5001"
commentaire_bp = Blueprint("commentaire_bp", __name__)

@commentaire_bp.route("/ajouter-commentaire", methods=["POST"])
def route_ajouter_commentaire():
    """
    Route pour ajouter un commentaire
    :return:
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token manquant"}), 401
    try:
        donnees = request.get_json()
        reponse = requests.post(f"{URL_SERVICE_LIVRAISON}/ajouter-commentaire", headers={"Authorization": token}, json=donnees)
        return jsonify(reponse.json()), reponse.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": "Erreur de communication avec le microservice",
            "details": str(e)
        }), 500

@commentaire_bp.route("/modifier-commentaire/<int:id>", methods=["PUT"])
def route_modifier_commentaire(id):
    """
    Route pour modifier un commentaire grace a l'id
    :param id:
    :return:
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token manquant"}), 401
    try:
        donnees = request.get_json()
        reponse = requests.put(f"{URL_SERVICE_LIVRAISON}/modifier-commentaire/{id}", headers={"Authorization": token},
                                json=donnees)
        return jsonify(reponse.json()), reponse.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": "Erreur de communication avec le microservice",
            "details": str(e)
        }), 500