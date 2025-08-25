from flask import Blueprint

from services.crud.crud_commentaire import *

commentaire_bp = Blueprint('commentaire', __name__)

@commentaire_bp.route('/commentaire', methods=['POST'])
def ajouter_commentaire_route():
    commentaire = ajouter_commentaire()
    return commentaire

@commentaire_bp.route('/commentaires/<int:utilisateur_id>', methods=['GET'])
def afficher_commentaire_route(utilisateur_id):
    """
        router pour recupere les commentaires d'un client
    """
    commentaires = afficher_commentaire(utilisateur_id)
    return commentaires

@commentaire_bp.route('/supprimer/<int:id>', methods=['POST'])
def supprimer_commentaire_route(id):
    supprimer = archiver_commentaire(id)
    return supprimer