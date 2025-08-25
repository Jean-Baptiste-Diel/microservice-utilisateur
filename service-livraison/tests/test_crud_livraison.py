import unittest

from flask import json

from app import creation_app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Création de l'application de test
        self.app = creation_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL'  # PostreSQL database
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

    def test_ajouter_livraison(self):
        donnee_test = {
            'client_id': '1',
            'livreur_id': '2',
        }
        # Envoi de la requête
        response = self.client.post(
            '/livraison',
            data=json.dumps(donnee_test),
            content_type='application/json'
        )
        # Vérifications
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        print("Test création livraison - Réussi")
if __name__ == '__main__':
    unittest.main()
