from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from services.authentification import connexion, deconnexion
from services.crud.crud_livreur import creation_livreur
from services.crud.crud_manageur import creation_manageur
from services.crud.crud_utilisateur import creation_utilisateur, archiver_utilisateur, mettre_a_jour_utilisateur

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/connexion', methods=['POST'])
def connexion_route():
    connexion_utilisateur = connexion()
    return connexion_utilisateur

@auth_bp.route('/creer-un-compte', methods=["POST"])
def creation_route():
    creation = creation_utilisateur()
    return creation

@auth_bp.route('/supprimer-compte/<int:id>', methods=["POST"])
def supprimer_route():
    archiver = archiver_utilisateur(id)
    return archiver

@auth_bp.route('/modifier/<int:id_utilisateur>', methods=["POST"])
def modifier_route(id_utilisateur=None):
    modifier = mettre_a_jour_utilisateur(id_utilisateur)
    return modifier

@auth_bp.route('/creation-manageur', methods=["POST"])
def creation_manageur_route():
    creation_utilisateur_mangeur = creation_manageur()
    return creation_utilisateur_mangeur

@auth_bp.route('/deconnexion', methods=["POST"])
def deconnexion_route():
    deconnexion_utilisateur = deconnexion()
    return deconnexion_utilisateur

@auth_bp.route('/creation-livreur/<int:manageur_id>', methods=["POST"])
@jwt_required()
def creation_livreur_route(manageur_id):
    try:
        # 1. Vérification JWT et permissions
        claims = get_jwt()
        if claims.get('role') != 'Manageur' or claims.get('user_id') != manageur_id:
            return jsonify({"error": "Action non autorisée"}), 403
        # 2. Passe la main à la fonction de service
        return creation_livreur(manageur_id, request.get_json())
    except Exception as e:
        return jsonify({"message": "Erreur serveur",
                        "details": e}), 500