import json
import unittest
import unittest
from flask import json
from app import creation_app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Création de l'application de test
        self.app = creation_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/memoire_microservice_utilisateur'  # PostreSQL database
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

    def test_connexion_success(self):
            # Données valides
        data = {
            "email": "jean@gmail.com",  # Correction: "email" au lieu de "nom"
            "mot_de_passe": "diel123"
        }

        response = self.client.post('/connexion',
            data=json.dumps(data),
            content_type='application/json'
        )

            # Debug
        print("Statut HTTP:", response.status_code)
        print("Réponse JSON:", response.get_json())

            # Assertions
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['message'], "Identifiant valide")
        self.assertEqual(json_data['utilisateur']['email'], "jean@gmail.com")

    def test_connexion_invalid_password(self):
            # Mot de passe incorrect
        data = {
            "email": "jean@gmail.com",
            "mot_de_passe": "mauvaispassword"
        }

        response = self.client.post('/connexion',
            data=json.dumps(data),
            content_type='application/json'
        )

        print("Réponse JSON:", response.get_json())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['message'], "Identifiant invalide")

    def test_connexion_missing_fields(self):
            # Test avec des champs manquants
        test_cases = [
            {"email": "jean@gmail.com"},  # Manque mot_de_passe
            {"mot_de_passe": ""},  # Manque email
            {}  # Tous les champs manquants
        ]

        for case in test_cases:
            response = self.client.post('/connexion',
                data=json.dumps(case),
                content_type='application/json'
            )
        print("Réponse JSON:", response.get_json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], "Tous les champs sont requis")




if __name__ == '__main__':
    unittest.main()
