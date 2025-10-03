import unittest


# python
import unittest
from datetime import datetime, timezone, timedelta

from flask import json
from flask_jwt_extended import create_access_token

from app import creation_app
from configs.config import db
from models import Livraison, Commentaire, Statistique


class StatistiquesApiTestCase(unittest.TestCase):
    def setUp(self):
        # App et base en mémoire
        self.app = creation_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # Important pour create_access_token
        self.app.config['JWT_SECRET_KEY'] = 'test-secret'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        # Génère un token JWT pour les routes protégées
        with self.app.app_context():
            self.token = create_access_token(identity="test-user")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def _seed_livraison_et_commentaires(self, livreur_id: int, sentiments: list[bool]):
        """
        Crée une livraison et plusieurs commentaires pour un livreur donné.
        sentiments: liste de True/False représentant la prediction.
        """
        with self.app.app_context():
            liv = Livraison(livreur_id=livreur_id, client_id=1, status='livre')
            db.session.add(liv)
            db.session.flush()
            now = datetime.now(timezone.utc)
            for i, s in enumerate(sentiments):
                c = Commentaire(
                    commentaire=f"c{i}",
                    prediction=s,
                    status='DESARCHIVER',
                    creation_date=now - timedelta(minutes=(len(sentiments) - i)),
                    livraison_id=liv.id
                )
                db.session.add(c)
            db.session.commit()

    def test_get_stats_aucune_statistique_retourne_404(self):
        # Aucun commentaire/stat: GET doit renvoyer 404
        resp = self.client.get("/livreurs/99/stats")
        self.assertEqual(resp.status_code, 404)

    def test_recompute_one_puis_get_stats(self):
        # Arrange: 3 commentaires (2 True, 1 False) pour livreur 1
        self._seed_livraison_et_commentaires(livreur_id=1, sentiments=[True, False, True])

        # Act: recalcul ciblé
        resp = self.client.post("/livreurs/1/stats/recompute", headers=self._auth_headers())
        self.assertEqual(resp.status_code, 200, resp.data)

        # Assert: GET renvoie les valeurs attendues
        resp = self.client.get("/livreurs/1/stats")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data["livreur_id"], 1)
        self.assertEqual(data["nombre_commentaires"], 3)
        self.assertAlmostEqual(data["moyenne_evaluation"], 2/3, places=5)
        self.assertIsNotNone(data["derniere_mise_a_jour"])

    def test_recompute_all_pour_plusieurs_livreurs(self):
        # Arrange
        self._seed_livraison_et_commentaires(livreur_id=1, sentiments=[True, True])     # moyenne 1.0
        self._seed_livraison_et_commentaires(livreur_id=2, sentiments=[False, True])    # moyenne 0.5

        # Act: recalcul global
        resp = self.client.post("/stats/recompute", headers=self._auth_headers())
        self.assertEqual(resp.status_code, 200)

        # Assert livreur 1
        resp1 = self.client.get("/livreurs/1/stats")
        self.assertEqual(resp1.status_code, 200)
        d1 = json.loads(resp1.data)
        self.assertEqual(d1["nombre_commentaires"], 2)
        self.assertAlmostEqual(d1["moyenne_evaluation"], 1.0, places=5)

        # Assert livreur 2
        resp2 = self.client.get("/livreurs/2/stats")
        self.assertEqual(resp2.status_code, 200)
        d2 = json.loads(resp2.data)
        self.assertEqual(d2["nombre_commentaires"], 2)
        self.assertAlmostEqual(d2["moyenne_evaluation"], 0.5, places=5)

    def test_recompute_one_remise_a_zero_si_aucun_commentaire(self):
        # Arrange: créer une ligne Statistique préexistante pour livreur 3
        with self.app.app_context():
            stat = Statistique(livreur_id=3, moyenne_evaluation=0.9, nombre_commentaires=10)
            db.session.add(stat)
            db.session.commit()

        # Act: recalcul ciblé sans aucun commentaire → doit remettre à zéro
        resp = self.client.post("/livreurs/3/stats/recompute", headers=self._auth_headers())
        self.assertEqual(resp.status_code, 200)

        # Assert: GET retourne 200 avec compte 0, moyenne 0.0, dernière maj None
        with self.app.app_context():
            stat_db = Statistique.query.filter_by(livreur_id=3).first()
            self.assertIsNotNone(stat_db)
            self.assertEqual(stat_db.nombre_commentaires, 0)
            self.assertEqual(stat_db.moyenne_evaluation, 0.0)
            self.assertIsNone(stat_db.derniere_mise_a_jour)

if __name__ == '__main__':
    unittest.main()