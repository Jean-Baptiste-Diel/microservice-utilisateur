from flask import Blueprint

from services.crud import crud_commentaire
commentaire_bp = Blueprint('commentaire', __name__)
@commentaire_bp.route('/commentaire', methods=['POST'])
def ajouter_commentaire_route():
    commentaire = crud_commentaire.ajouter_commentaire()
    return commentaire



@commentaire_bp.route('/supprimer/<int:id>', methods=['POST'])
def supprimer_commentaire_route(id):
    supprimer = crud_commentaire.archiver_commentaire(id)
    return supprimer