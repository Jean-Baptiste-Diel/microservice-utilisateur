# python
from sqlalchemy import func, case
from configs.config import db
from models import Commentaire, Livraison, Statistique

def _requete_agregation_de_base():
    """
    Retourne une requête agrégeant les commentaires par livreur.
    moyenne_evaluation: moyenne de sentiments (True=1, False=0).
    """
    return (
        db.session.query(
            Livraison.livreur_id.label("livreur_id"),
            func.count(Commentaire.id).label("nombre_commentaires"),
            func.avg(
                case(
                    (Commentaire.prediction == True, 1.0),
                    else_=0.0
                )
            ).label("moyenne_evaluation"),
            func.max(Commentaire.creation_date).label("derniere_mise_a_jour")
        )
        .join(Commentaire, Commentaire.livraison_id == Livraison.id)
        .group_by(Livraison.livreur_id)
    )

def recalculer_toutes_les_statistiques():
    """
    Recalcule la table Statistique pour tous les livreurs ayant au moins un commentaire.
    """
    rows = _requete_agregation_de_base().all()
    livreur_ids_seen = set()

    for row in rows:
        livreur_ids_seen.add(row.livreur_id)
        stat = Statistique.query.filter_by(livreur_id=row.livreur_id).first()
        if not stat:
            stat = Statistique(livreur_id=row.livreur_id)
            db.session.add(stat)
        stat.moyenne_evaluation = float(row.moyenne_evaluation or 0.0)
        stat.nombre_commentaires = int(row.nombre_commentaires or 0)
        stat.derniere_mise_a_jour = row.derniere_mise_a_jour
    db.session.commit()

def recalculer_statistiques_pour_livreur(livreur_id: int):
    """
    Recalcule les stats pour un livreur précis.
    """
    row = (
        _requete_agregation_de_base()
        .filter(Livraison.livreur_id == livreur_id)
        .first()
    )
    stat = Statistique.query.filter_by(livreur_id=livreur_id).first()
    if not row:
        # Aucun commentaire: on met à zéro ou on supprime la ligne (au choix).
        if stat:
            stat.moyenne_evaluation = 0.0
            stat.nombre_commentaires = 0
            stat.derniere_mise_a_jour = None
            db.session.commit()
        else:
            # Rien à faire si pas de ligne
            pass
        return

    if not stat:
        stat = Statistique(livreur_id=livreur_id)
        db.session.add(stat)

    stat.moyenne_evaluation = float(row.moyenne_evaluation or 0.0)
    stat.nombre_commentaires = int(row.nombre_commentaires or 0)
    stat.derniere_mise_a_jour = row.derniere_mise_a_jour
    db.session.commit()

def recuperer_statistiques_pour_livreur(livreur_id: int) -> dict | None:
    """
    Retourne les stats de la table Statistique (rapide).
    """
    stat = Statistique.query.filter_by(livreur_id=livreur_id).first()
    if not stat:
        return None
    return {
        "livreur_id": stat.livreur_id,
        "moyenne_evaluation": stat.moyenne_evaluation,
        "nombre_commentaires": stat.nombre_commentaires,
        "derniere_mise_a_jour": stat.derniere_mise_a_jour.isoformat() if stat.derniere_mise_a_jour else None,
    }