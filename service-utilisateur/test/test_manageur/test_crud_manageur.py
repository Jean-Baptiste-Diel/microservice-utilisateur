import unittest

from flask_jwt_extended import create_access_token

from app import creation_app
from models import db, Role
import json


class TestManageurCreation(unittest.TestCase):
    def setUp(self):
        self.app = creation_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

    def test_creation_utilisateur_manageur(self):
        test_data = {
            "nom": "manageur",
            "prenom": "Diel",
            "email": "diel49o@gmail.com",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "role_id": 3
        }
        # 2. Création d'un token de manageur valide
        with self.app.app_context():
            manageur_token = create_access_token(
                identity=test_data['email'],
                additional_claims={
                    "role": "Manageur"
                }
            )
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creation-manageur',
                data=json.dumps(test_data),
                content_type='application/json',
                headers = {'Authorization': f'Bearer {manageur_token}'}
            )
            print(response.data)  # Debug
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)
            self.assertEqual(response_data['message'], "Manager créé avec succès")

    def test_creation_utilisateur_manageur_email_invalide(self):
        test_data = {
            "nom": "manageur",
            "prenom": "Diel",
            "email": "diele",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "role_id": 3
        }
        # 2. Création d'un token de manageur valide
        with self.app.app_context():
            manageur_token = create_access_token(
                identity=test_data['email'],
                additional_claims={
                    "role": "Manageur"
                }
            )
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creation-manageur',
                data=json.dumps(test_data),
                content_type='application/json',
                headers = {'Authorization': f'Bearer {manageur_token}'}
            )
            # Debug
            print("Status Code:", response.status_code)
            print("Response Data:", response.get_json())
            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)

    def test_creation_utilisateur_manageur_donnee_manquante(self):
        test_data = {
            "prenom": "Diel",
            "email": "diele",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "role_id": 3
        }
        # 2. Création d'un token de manageur valide
        with self.app.app_context():
            manageur_token = create_access_token(
                identity=test_data['email'],
                additional_claims={
                    "role": "Manageur"
                }
            )
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creation-manageur',
                data=json.dumps(test_data),
                content_type='application/json',
                headers = {'Authorization': f'Bearer {manageur_token}'}
            )
            # Debug
            print("Status Code:", response.status_code)
            print("Response Data:", response.get_json())
            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)
            self.assertEqual(response_data['message'], "Champs manquants")
if __name__ == '__main__':
    unittest.main()