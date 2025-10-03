from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from services.authentification import connexion, deconnexion
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
@jwt_required()
def supprimer_route(utilisateur_id):
    try:
        claims = get_jwt()
        if claims.get('role') != 'Manageur' or claims.get('user_id') != utilisateur_id:
            return jsonify({"error": "Action non autorisée"}), 403
        archiver = archiver_utilisateur(id)
        return archiver
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@auth_bp.route('/modifier/<int:id_utilisateur>', methods=["POST"])
@jwt_required()
def modifier_route(id_utilisateur=None):
    modifier = mettre_a_jour_utilisateur(id_utilisateur)
    return modifier

@auth_bp.route('/deconnexion', methods=["POST"])
@jwt_required()
def deconnexion_route(utilisateur_id):
    try:
        claims = get_jwt()
        if claims.get('role') != 'Manageur' or claims.get('user_id') != utilisateur_id:
            return jsonify({"error": "Action non autorisée"}), 403
        deconnexion_utilisateur = deconnexion()
        return deconnexion_utilisateur
    except Exception as e:
        return jsonify({"error": str(e)}), 500
