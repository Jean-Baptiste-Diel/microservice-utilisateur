from flask import Blueprint

from services.crud.crud_livraison import ajouter_livraison

livraison_bp = Blueprint('livraison_bp', __name__)

@livraison_bp.route('/livraison', methods=['POST'])
def creer_livraison_route():
    creer_livraison = ajouter_livraison()
    return creer_livraison