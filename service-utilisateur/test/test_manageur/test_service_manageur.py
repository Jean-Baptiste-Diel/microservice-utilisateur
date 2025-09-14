import unittest
import json
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# --- Mock fonction afficher_livreurs ---
def afficher_livreurs(manageur_id):
    return [{"id": 1, "nom": "Livreur 1"}, {"id": 2, "nom": "Livreur 2"}]

# --- Création de l'app de test ---
def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test_secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    JWTManager(app)

    @app.route('/livreurs')
    @jwt_required()
    def livres():
        claims = get_jwt_identity()
        if claims.get("role") != "Manageur":
            return jsonify({"error": "Action non autorisée"}), 403
        manageur_id = claims.get("id")
        return jsonify(afficher_livreurs(manageur_id)), 200

    return app


class TestLivreursEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_test_app()
        self.client = self.app.test_client()

    def test_get_livreurs_authorized(self):
        with self.app.app_context():
            token = create_access_token(identity={"id": 55, "email": "diel49o@gmail.com", "role": "Manageur"})
            response = self.client.get("/livreurs", headers={"Authorization": f"Bearer {token}"})
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            self.assertIn("nom", data[0])

    def test_get_livreurs_missing_token(self):
        response = self.client.get("/livreurs")
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn("Missing Authorization Header", data.get("msg", ""))

    def test_get_livreurs_invalid_role(self):
        with self.app.app_context():
            token = create_access_token(identity={"id": 99, "email": "user@test.com", "role": "Client"})
            response = self.client.get("/livreurs", headers={"Authorization": f"Bearer {token}"})
            self.assertEqual(response.status_code, 403)
            data = json.loads(response.data)
            self.assertEqual(data["error"], "Action non autorisée")


if __name__ == "__main__":
    unittest.main()
