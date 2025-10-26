from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from flask import jsonify
from configs.config import db
from models import Livreur, Utilisateur, Manageur


# Changer le statut du livreur
def bloquer_livreur(utilisateur_id):
    try:
        utilateur = Utilisateur.query.get(utilisateur_id)
        if utilateur is None:
            return jsonify({"message": "Livreur introuvable"}), 400
        Utilisateur.status = 'ARCHIVER'
        db.session.commit()
        return jsonify({"livreur": utilateur})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

def rechercher_livreur(terme):
    try:
        terme = f"%{terme}%"
        livreurs = (db.session.query(Livreur)
                    .join(Utilisateur, Utilisateur.id == Livreur.utilisateur_id)
                    .filter(or_(
                        Utilisateur.nom.ilike(terme),
                        Utilisateur.prenom.ilike(terme),
                        Utilisateur.email.ilike(terme)
                    )).all())
        if not livreurs:
            return jsonify({"message": "Livreur introuvable"}), 404
        return jsonify([livreur.to_dict() for livreur in livreurs]), 200
    except SQLAlchemyError as e:
        return jsonify({"message": str(e)}), 500

def afficher_livreur(livreur_id):
    try:
        livreur = db.session.get(Livreur, livreur_id)
        if not livreur:
            return jsonify({"message": "Livreur introuvable"}), 404
        return jsonify(livreur.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({"message": str(e)}), 500

def afficher_livreurs(manageur_id):
    try:
        manageur = Manageur.query.filter_by(utilisateur_id=manageur_id).first()
        liveurs = (db.session.query(Livreur)
            .join(Utilisateur, Utilisateur.id == Livreur.utilisateur_id)
            .filter(Livreur.manageur_id == manageur.id)).all()
        print(liveurs)
        return jsonify([liveur.to_dict() for liveur in liveurs]), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


def afficher_livreurs1():
    try:
        manageurs = Manageur.query.all()
        return jsonify([manageur.to_dict() for manageur in manageurs]), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500