import os
import unittest
import json
from app import creation_app

class TestClientCreation(unittest.TestCase):
    def setUp(self):
        self.app = creation_app()
        self.app.config['TESTING'] = True
        database_url = os.environ.get('DATABASE_URL')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

    def test_creation_utilisateur_client(self):
        test_data = {
            "nom": "client",
            "prenom": "Diel",
            "email": "diel049700@gmail.com",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "adresse": "medina",
            "role_id": 3
        }
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creer-client',
                data=json.dumps(test_data),
                content_type='application/json'
            )
            # Debug
            print("Status Code:", response.status_code)
            print("Response Data:", response.get_json())
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)
            self.assertEqual(response_data['message'], "Client créé avec succès")

    def test_creation_client_donnee_manquante(self):
        test_data = {
            "nom": "client",
            "prenom": "Diel",
            "mot_de_passe": "diel123",
            "adresse": "medina",
            "role_id": 3
        }
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creer-client',
                data=json.dumps(test_data),
                content_type='application/json'
            )
            # Debug
            print("Status Code:", response.status_code)
            print("Response Data:", response.get_json())
            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)
            self.assertEqual(response_data['message'], "Champs manquants")

    def test_creation_client_email_invalide_format(self):
            test_data = {
                "nom": "client",
                "prenom": "Diel",
                "email": "diel06",
                "mot_de_passe": "diel123",
                "adresse": "medina",
                "role_id": 3
            }
            # Nouveau bloc with pour gérer le contexte
            with self.app.app_context():
                response = self.client.post(
                    '/creer-client',
                    data=json.dumps(test_data),
                    content_type='application/json'
                )
                # Debug
                print("Status Code:", response.status_code)
                print("Response Data:", response.get_json())
                self.assertEqual(response.status_code, 400)
                response_data = json.loads(response.data)
                self.assertIn('message', response_data)
                self.assertEqual(response_data['message'], "Format d'email invalide")

    def test_creation_utilisateur_client_email_utiliser(self):
        test_data = {
            "nom": "client",
            "prenom": "Diel",
            "email": "diel0490@gmail.com",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "adresse": "medina",
            "role_id": 3
        }
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creer-client',
                data=json.dumps(test_data),
                content_type='application/json'
            )
            # Debug
            print("Status Code:", response.status_code)
            print("Response Data:", response.get_json())
            self.assertEqual(response.status_code, 409)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)
            self.assertEqual(response_data['message'], "Cet email est déjà utilisé")

if __name__ == '__main__':
    unittest.main()
