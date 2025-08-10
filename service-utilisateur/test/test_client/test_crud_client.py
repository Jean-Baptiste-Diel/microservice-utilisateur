import unittest
import json
from app import creation_app
from configs.config import db


class TestClientCreation(unittest.TestCase):
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

    def test_creation_utilisateur_client(self):
        test_data = {
            "nom": "client",
            "prenom": "Diel",
            "email": "diel090@gmail.com",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "adresse": "medina",
            "role_id": 3
        }
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creer',
                data=json.dumps(test_data),
                content_type='application/json'
            )

            print(response.data)  # Debug

            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)
            self.assertEqual(response_data['message'], "Client créé avec succès")

if __name__ == '__main__':
    unittest.main()
