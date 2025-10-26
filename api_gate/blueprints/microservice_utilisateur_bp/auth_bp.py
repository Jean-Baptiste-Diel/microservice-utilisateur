import requests
from flask import Blueprint, jsonify, request

URL_SERVICE_UTILISATETEUR = "http://localhost:5000"
URL_SERVICE_LIVRAISON = "http://localhost:5001"
auth_bp = Blueprint('auth_bp', __name__)
@auth_bp.route('/connexion', methods=['POST'])
def connexion():
    donnees = request.get_json()
    reponse = requests.post(f"{URL_SERVICE_UTILISATETEUR}/connexion", json=donnees)
    return jsonify(reponse.json()), reponse.status_code