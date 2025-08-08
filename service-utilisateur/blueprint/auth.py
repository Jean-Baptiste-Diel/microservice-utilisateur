from flask import Blueprint

from services.authentification import connexion

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/connexion', methods=["POST"])
def connexion_route():
    connexion_utilisateur = connexion()
    return connexion_utilisateur