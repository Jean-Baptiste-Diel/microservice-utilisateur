from datetime import datetime, timezone
from configs.config import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nom_du_role = db.Column(db.String(50), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    utilisateurs = db.relationship('Utilisateur', back_populates='role', lazy='dynamic')


class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(20), default="ACTIVE", nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    # Relations
    role = db.relationship('Role', back_populates='utilisateurs', lazy='joined')
    client = db.relationship('Client', back_populates='utilisateur', uselist=False, cascade='all, delete-orphan')
    manageur = db.relationship('Manageur', back_populates='utilisateur', uselist=False, cascade='all, delete-orphan')
    livreur = db.relationship('Livreur', back_populates='utilisateur', uselist=False, cascade='all, delete-orphan')


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    lieu_livraison = db.Column(db.String(100), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), unique=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    utilisateur = db.relationship('Utilisateur', back_populates='client')


class Manageur(db.Model):
    __tablename__ = 'manageurs'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), unique=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    utilisateur = db.relationship('Utilisateur', back_populates='manageur')
    livreurs = db.relationship('Livreur', back_populates='manageur')


class Livreur(db.Model):
    __tablename__ = 'livreurs'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), unique=True)
    manageur_id = db.Column(db.Integer, db.ForeignKey('manageurs.id'))
    creation_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    utilisateur = db.relationship('Utilisateur', back_populates='livreur')
    manageur = db.relationship('Manageur', back_populates='livreurs')