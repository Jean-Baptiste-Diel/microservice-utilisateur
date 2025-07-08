from datetime import datetime, timezone
from configs.config import db


class Role(db.Model):
    __tablename__ = 'roles'  # Toujours utiliser le pluriel pour les noms de table

    id = db.Column(db.Integer, primary_key=True)
    nom_du_role = db.Column(db.String(50), unique=True, nullable=False)  # Longueur max spécifiée
    creation_date = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),  # Lambda pour éviter le même timestamp pour tous
        index=True  # Index pour les requêtes fréquentes
    )

    # Relation avec Utilisateur
    utilisateurs = db.relationship(
        'Utilisateur',
        back_populates='role',  # Plus explicite que backref
        lazy='dynamic',  # Chargement différé
        cascade='all, delete-orphan'  # Gestion des dépendances
    )


class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)  # Longueur max
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Longueur standard email
    mot_de_passe = db.Column(db.String(128), nullable=False)  # Longueur pour hash bcrypt
    status = db.Column(db.String(20), default="ACTIVE", nullable=False, index=True  # Index pour les requêtes de statut
    )
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id'),
        nullable=False
    )
    creation_date = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    # Relation avec Role
    role = db.relationship(
        'Role',
        back_populates='utilisateurs',  # Correspond au champ dans Role
        lazy='joined'  # Chargement immédiat par défaut
    )