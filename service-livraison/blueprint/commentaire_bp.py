from flask import Blueprint, request

from services.crud_commentaire import ajouter_commentaire

commentaire_bp = Blueprint('commentaire', __name__)

@commentaire_bp.route('/commentaire', methods=['POST'])
def ajouter_commentaire_route():
    commentaire = ajouter_commentaire()
    return commentaire

@commentaire_bp.route('/commentaires', methods=['POST'])
def creer_commentaire():
    # Récupération des données
    data = request.get_json()
    return data