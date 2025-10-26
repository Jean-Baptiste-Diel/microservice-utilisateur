import requests
from flask import Blueprint, jsonify, request

livraison_bp = Blueprint('livraison_bp', __name__)
URL_SERVICE_LIVRAISON = "http://localhost:5001"
URL_SERVICE_UTILISATETEUR = "http://localhost:5000/"

@livraison_bp.route('/livraisons', methods=['GET'])
def route_livraisons():
    """
    Recuper et envoie les livraison et le commentaire
    :return: livraisons json
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token manquant"}), 401
    try:
        resp = requests.get(f"{URL_SERVICE_LIVRAISON}/livraisons", headers={"Authorization": token})
        # Retourner la réponse telle quelle
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": "Erreur de communication avec le microservice livraison",
            "details": str(e)
        }), 500

@livraison_bp.route("/info-livraison", methods=["GET"])
def livraisons_completes():
    """
    Route pour recuperer les information complete
    d'une livraison pour l'afficher chez le client
    :return: livraisons json
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token manquant"}), 401
    try:
        # Récupérer les livraisons depuis le microservice Livraison
        livraisons_resp = requests.get(f"{URL_SERVICE_LIVRAISON}/livraisons", headers={"Authorization": token})
        print("Status code livraisons:", livraisons_resp.status_code)
        print("Réponse livraisons:", livraisons_resp.text)
        if livraisons_resp.status_code != 200:
            return jsonify({"error": "Impossible de récupérer les livraisons"}), 500
        livraisons = livraisons_resp.json()
        result = []
        for livraison in livraisons:
            livreur_id = livraison["livreur_id"]
            client_id = livraison["client_id"]
            # Récupérer les infos du livreur depuis le microservice Utilisateur
            if client_id:
                # information livreur a afficher cher le client
                user_resp = requests.get(f"{URL_SERVICE_UTILISATETEUR}/livreur/{livreur_id}",
                                         headers={"Authorization": token})
                print(f"Status code utilisateur {livreur_id}:", user_resp.status_code)
                print(f"Réponse utilisateur {livreur_id}:", user_resp.text)
            else:
                # information client a afficher cher le livreur
                user_resp = requests.get(f"{URL_SERVICE_UTILISATETEUR}/client/{client_id}", headers={"Authorization": token})
                print(f"Status code utilisateur {client_id}:", user_resp.status_code)
                print(f"Réponse utilisateur {client_id}:", user_resp.text)
            if user_resp.status_code == 200:
                client_data = user_resp.json()
            else:
                client_data = {"nom": "Inconnu", "adresse": "Inconnue"}
            # Fusionner les données
            livraison_complete = {**livraison, "client": client_data}
            result.append(livraison_complete)
        # Retourner la réponse complète
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": "Erreur de communication avec le microservice",
            "details": str(e)
        }), 500

@livraison_bp.route("/info1-livraison", methods=["GET"])
def livraisons_completes1():
    """
    Route pour recuperer les information complete
    d'une livraison pour l'afficher chez le livreur
    :return: livraisons json
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token manquant"}), 401
    try:
        # Récupérer les livraisons depuis le microservice Livraison
        livraisons_resp = requests.get(f"{URL_SERVICE_LIVRAISON}/livraisons", headers={"Authorization": token})
        print("Status code livraisons:", livraisons_resp.status_code)
        print("Réponse livraisons:", livraisons_resp.text)
        if livraisons_resp.status_code != 200:
            return jsonify({"error": "Impossible de récupérer les livraisons"}), 500
        livraisons = livraisons_resp.json()
        result = []
        for livraison in livraisons:
            client_id = livraison["client_id"]
            # Récupérer les infos du livreur depuis le microservice Utilisateur
            user_resp = requests.get(f"{URL_SERVICE_UTILISATETEUR}/client/{client_id}", headers={"Authorization": token})
            print(f"Status code utilisateur {client_id}:", user_resp.status_code)
            print(f"Réponse utilisateur {client_id}:", user_resp.text)
            if user_resp.status_code == 200:
                client_data = user_resp.json()
            else:
                client_data = {"nom": "Inconnu", "adresse": "Inconnue"}
            # Fusionner les données
            livraison_complete = {**livraison, "client": client_data}
            result.append(livraison_complete)
        # Retourner la réponse complète
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": "Erreur de communication avec le microservice",
            "details": str(e)
        }), 500