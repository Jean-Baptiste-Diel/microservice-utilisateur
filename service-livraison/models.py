from datetime import datetime, timezone
from configs.config import db

class Livraison(db.Model):
    __tablename__ = 'livraisons'

    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    livreur_id = db.Column(db.Integer)
    status = db.Column(db.String, nullable=False, default='non-livre')
    creation_date = db.Column(
        db.DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    # ✅ Relation 1→1 : une seule ligne liée dans Commentaire
    commentaire = db.relationship(
        'Commentaire',
        back_populates='livraison',
        uselist=False,           # 1 seul objet, pas une liste
        cascade="all, delete"
    )

    def to_dict(self):
        return {
            'id': self.id,
            'matricule': self.matricule,
            'client_id': self.client_id,
            'livreur_id': self.livreur_id,
            'creation_date': self.creation_date,
            'status': self.status,
            # ✅ renvoie le commentaire unique (ou None)
            'commentaire': self.commentaire.to_dict() if self.commentaire else None
        }


class Commentaire(db.Model):
    __tablename__ = 'commentaires'

    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String, nullable=False)
    prediction = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String, nullable=False, default='DESARCHIVER')
    creation_date = db.Column(
        db.DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    # ✅ Clé étrangère unique pour imposer 1 seul commentaire par livraison
    livraison_id = db.Column(
        db.Integer,
        db.ForeignKey('livraisons.id'),
        unique=True,            # 🔒 un seul commentaire par livraison
        nullable=False
    )

    # ✅ Relation inverse
    livraison = db.relationship(
        'Livraison',
        back_populates='commentaire'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'commentaire': self.commentaire,
            'prediction': self.prediction,
            'status': self.status,
            'creation_date': self.creation_date.isoformat(),
            'livraison_id': self.livraison_id
        }

class Statistique(db.Model):
    __tablename__ = 'statistiques'
    id = db.Column(db.Integer, primary_key=True)
    livreur_id = db.Column(db.Integer)
    moyenne_evaluation = db.Column(db.Float, nullable=False, default=0.0)
    nombre_commentaires = db.Column(db.Integer, nullable=False, default=0)
    derniere_mise_a_jour = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)