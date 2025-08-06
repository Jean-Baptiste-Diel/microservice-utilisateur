import unittest
from app import creation_app
from models import db, Role
import json


class TestManageurCreation(unittest.TestCase):
    def setUp(self):
        self.app = creation_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/memoire_microservice_utilisateur'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.rollback()  # Annule toute transaction active
            db.session.remove()

    def test_creation_utilisateur_manageur(self):
        test_data = {
            "nom": "manageur",
            "prenom": "Diel",
            "email": "diel8@gmail.com",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "role_id": 3
        }
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creation-manageur',
                data=json.dumps(test_data),
                content_type='application/json'
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
            "email": "diele@gmail.com",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "role_id": 3
        }
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creation-manageur',
                data=json.dumps(test_data),
                content_type='application/json'
            )
            print(response.data)  # Debug

            self.assertEqual(response.status_code, 409)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)
if __name__ == '__main__':
    unittest.main()