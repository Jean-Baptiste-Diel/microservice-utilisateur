
import unittest
import json
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
        test_data = {
            "nom": "livreur",
            "prenom": "Diel",
            "email": "liveur3_test@gmail.com",  # Changé pour être unique
            "mot_de_passe": "diel123",
            "role_id": 4
        }
        # Nouveau bloc with pour gérer le contexte
        with self.app.app_context():
            response = self.client.post(
                '/creation-livreur/2',
                data=json.dumps(test_data),
                content_type='application/json'
            )
            print(response.data)  # Debug
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.data)
            self.assertIn('message', response_data)
            self.assertEqual(response_data['message'], "Livreur créé avec succès")


if __name__ == '__main__':
    unittest.main()