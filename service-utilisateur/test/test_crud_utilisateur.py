import unittest
from flask import json
from app import creation_app
from configs.config import db


class TestUtilisateurRoutes(unittest.TestCase):
    def setUp(self):
        # Création de l'application de test
        self.app = creation_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.client = self.app.test_client()

    def test_creation_utilisateur(self):
        """Test la création d'un utilisateur"""
        test_data = {
            "nom": "INANG",
            "prenom": "Diel",
            "email": "jean@gmail.com",
            "mot_de_passe": "diel123",
            "role_id": 1
        }

        # Envoi de la requête
        response = self.client.post(
            '/creer-un-compte',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        # Vérifications
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('id', response_data)
        print("Test création utilisateur - Réussi")

    def test_creation_utilisateur_donnees_invalides(self):
        """Test avec des données invalides"""
        test_data = {
            "nom": "",  # Nom vide
            "prenom": "Diel",
            "email": "email_invalide",
            "mot_de_passe": "short",
            "role_id": 1
        }

        response = self.client.post(
            '/creer-un-compte',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        print("Test données invalides - Réussi")


if __name__ == '__main__':
    unittest.main()