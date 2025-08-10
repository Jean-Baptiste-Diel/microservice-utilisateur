
import unittest
import json
import uuid

from flask_jwt_extended import create_access_token

from app import creation_app
from models import db, Utilisateur, Role, Manageur, Livreur
import bcrypt


class TestLivreurEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = creation_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/memoire_microservice_utilisateur'  # PostreSQL database

        self.client = self.app.test_client()

    def test_creation_utilisateur_livreur(self):
        # 1. Préparation des données de test
        test_data = {
            "nom": "livreur",
            "prenom": "Diel",
            "email": "livreur_test_3484@gmail.com".format(uuid.uuid4().hex[:8]),  # Email unique
            "mot_de_passe": "diel123",
            "role_id": 4  # ID du rôle livreur
        }

        # 2. Création d'un token de manageur valide
        with self.app.app_context():
            manageur_token = create_access_token(
                identity="diel@gmail.com",
                additional_claims={
                    "user_id": 3,  # Correspond au manageur_id dans la route
                    "role": "Manageur"
                }
            )

        # 3. Exécution de la requête
        with self.app.app_context():
            response = self.client.post(
                '/creation-livreur/3',  # Doit correspondre au user_id dans le token
                data=json.dumps(test_data),
                content_type='application/json',
                headers={'Authorization': f'Bearer {manageur_token}'}
            )

            # Debug
            print("Status Code:", response.status_code)
            print("Response Data:", response.get_json())

            # 4. Assertions
            self.assertEqual(response.status_code, 201)
            response_data = response.get_json()
            self.assertEqual(response_data['message'], "Livreur créé avec succès")
            self.assertIn('livreur', response_data)
            self.assertEqual(response_data['livreur']['manageur_id'], 3)


if __name__ == '__main__':
    unittest.main()