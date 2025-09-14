import random
from datetime import datetime, timedelta, timezone

from configs.config import db
from models import Livraison, Statistique, Commentaire


def seed_database():
    """Seed des livraisons et commentaires avec IDs factices"""
    if Livraison.query.count() == 0:
        print("Création des livraisons...")

        # IDs factices pour clients et livreurs (simuler les IDs du service utilisateur)
        client_ids = [1, 2, 3]  # IDs factices de clients
        livreur_ids = [1, 2, 3]  # IDs factices de livreurs
        livreur_noms = {
            1: "Luc Bernard",
            2: "Sophie Petit",
            3: "Jean Robert"
        }

        livraisons = []
        matricule_counter = 1000

        # Textes de commentaires
        commentaires_positifs = [
            "Livraison rapide et efficace", "Très bon service, je recommande",
            "Colis en parfait état, merci", "Livreur très professionnel",
            "Excellent, rien à redire", "Service ponctuel et courtois",
            "Parfait, merci beaucoup", "Très satisfait du service",
            "Livraison avant l'heure prévue", "Emballage soigné et sécurisé"
        ]

        commentaires_negatifs = [
            "Livreur en retard de 2 heures", "Colis endommagé à la réception",
            "Livreur peu aimable et pressé", "Retard important sur la livraison",
            "Produit manquant dans le colis", "Service médiocre"
        ]

        # Créer des livraisons
        for i in range(20):  # 20 livraisons au total
            client_id = random.choice(client_ids)
            livreur_id = random.choice(livreur_ids)

            # Date aléatoire dans les 30 derniers jours
            random_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))

            livraison = Livraison(
                matricule=matricule_counter,
                client_id=client_id,
                livreur_id=livreur_id,
                status='livrée',
                creation_date=random_date
            )
            livraisons.append(livraison)
            db.session.add(livraison)
            matricule_counter += 1

        db.session.commit()
        print(f"{len(livraisons)} livraisons créées avec succès!")

        # Création des commentaires
        print("Création des commentaires...")
        commentaires_crees = 0

        for livraison in livraisons:
            # 70% de chance d'avoir un commentaire
            if random.random() < 0.7:
                # 80% de commentaires positifs, 20% négatifs
                if random.random() < 0.8:
                    commentaire_text = random.choice(commentaires_positifs)
                    prediction = True
                else:
                    commentaire_text = random.choice(commentaires_negatifs)
                    prediction = False

                comment_date = livraison.creation_date + timedelta(hours=random.randint(1, 48))

                commentaire = Commentaire(
                    commentaire=commentaire_text,
                    prediction=prediction,
                    status='DESARCHIVER',
                    livraison_id=livraison.id,
                    creation_date=comment_date
                )
                db.session.add(commentaire)
                commentaires_crees += 1

        db.session.commit()
        print(f"{commentaires_crees} commentaires créés avec succès!")

    else:
        print("Les livraisons existent déjà.")


def seed_statistiques():
    """Seed des statistiques basées sur les commentaires existants"""
    if Statistique.query.count() == 0:
        print("Calcul des statistiques...")

        # IDs et noms factices des livreurs
        livreur_stats = {
            1: {"nom": "Luc Bernard", "positifs": 0, "total": 0},
            2: {"nom": "Sophie Petit", "positifs": 0, "total": 0},
            3: {"nom": "Jean Robert", "positifs": 0, "total": 0}
        }

        # Compter les commentaires par livreur
        commentaires = Commentaire.query.join(Livraison).all()

        for commentaire in commentaires:
            livreur_id = commentaire.livraison.livreur_id
            if livreur_id in livreur_stats:
                livreur_stats[livreur_id]["total"] += 1
                if commentaire.evaluation == 1:
                    livreur_stats[livreur_id]["positifs"] += 1

        # Créer les statistiques
        for livreur_id, stats in livreur_stats.items():
            if stats["total"] > 0:
                moyenne = stats["positifs"] / stats["total"]
            else:
                moyenne = 0.0

            statistique = Statistique(
                livreur_id=livreur_id,
                livreur_nom=stats["nom"],
                moyenne_evaluation=round(moyenne, 2),
                nombre_commentaires=stats["total"],
                derniere_mise_a_jour=datetime.now(timezone.utc)
            )
            db.session.add(statistique)

        db.session.commit()
        print("Statistiques calculées avec succès!")
    else:
        print("Les statistiques existent déjà.")