from flask import Blueprint

from services.crud.crud_client import creation_client

client_bp = Blueprint('client', __name__)

@client_bp.route('/creer-client', methods=["POST"])
def creer_client_route():
    creer_client = creation_client()
    return creer_client