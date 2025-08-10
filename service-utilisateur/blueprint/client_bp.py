from flask import Blueprint

from services.crud.crud_client import creation_client

client_bp = Blueprint('client', __name__)

@client_bp.route('/creer')
def creer_client_route():

    return "creer_client"