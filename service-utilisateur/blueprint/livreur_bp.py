from flask import blueprints

livreur_bp = blueprints.Blueprint('livreur_bp', __name__)

@livreur_bp.route("/livreur")
def livreur():
    """TODO document why this method is empty"""
    pass

