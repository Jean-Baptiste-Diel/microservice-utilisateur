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

    def test_ajouter_commentaire(self):
        donnee_test = {
            'commentaire': 'Correct mais emballage un peu léger pour un produit fragile',
            'livraison_id': '1',
        }
        # Envoi de la requête
        response = self.client.post(
            '/commentaire',
            data=json.dumps(donnee_test),
            content_type='application/json'
        )
        # Vérifications
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        print("Test création livraison - Réussi")

    def test_afficher_commentaire_client_livrer(self):
        donnee_test = {'livraison_id': 1}
        response = self.client.get(
            '/commentaires/1',
            data=json.dumps(donnee_test),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        print("Test afficher livraison", response_data)

    def test_archiver_commentaire(self):
        donnee_test = {'id': 2}
        response = self.client.post(
            '/supprimer/2',
            data=json.dumps(donnee_test),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        print("Test archiver commentaire", response_data.message)
if __name__ == '__main__':
    unittest.main()
