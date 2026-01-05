import requests
from flask import Flask, jsonify
from flask_cors import CORS

from blueprints.microservice_livraison_bp.commentaire_bp import commentaire_bp
from blueprints.microservice_livraison_bp.livraison_bp import livraison_bp
from blueprints.microservice_utilisateur_bp.manageur_bp import manageur_bp
from blueprints.microservice_utilisateur_bp.auth_bp import auth_bp

app = Flask(__name__)

# ✅ Configuration CORS
CORS(app,
    supports_credentials=True,
    resources={r"*": {"origins": ["http://localhost:4200"]}},
    expose_headers=["Authorization"])

app.register_blueprint(auth_bp)
app.register_blueprint(livraison_bp)
app.register_blueprint(commentaire_bp)
app.register_blueprint(manageur_bp)
@app.route('/')
def hello_world():
    return 'Hello World!'
URL_SERVICE_UTILISATETEUR = "http://localhost:5000"
URL_SERVICE_LIVRAISON = "http://localhost:5001"

@app.route("/livreurs1", methods=["GET"])
def livreurs1():
    print("livreurs1")
    livraisons_resp = requests.get(f"{URL_SERVICE_UTILISATETEUR}/livreurs1")
    livraisons = livraisons_resp.json()
    return jsonify(livraisons)

if __name__ == '__main__':
    app.run(port=5005, debug=True)
