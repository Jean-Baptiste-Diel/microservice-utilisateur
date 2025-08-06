import requests
from flask import jsonify, request


def get_id():
    try:
        # 1. Récupération des données
        data = request.get_json()
        # 2. Validation minimale
        if not data or 'livreur_id' not in data:
            return jsonify({"error": "livreur_id requis"}), 400
        payload = {
            "livreur_id": data['livreur_id'],
            "client_id": data['client_id'],
        }
        response = requests.post('http://service-commentaire:5000/commentaires',
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=3)
        # 5. Gestion des erreurs HTTP
        response.raise_for_status()
        # 6. Retour du résultat
        return jsonify({
            "status": "success",
            "commentaire_id": response.json().get('id')
        }), 201
    except requests.exceptions.RequestException as e:
        # Erreurs de connexion/timeout
        return jsonify({"error": f"Erreur service commentaire: {str(e)}"}), 502
    except Exception as e:
        # Erreurs inattendues
        return jsonify({"error": "Erreur interne"}), 500