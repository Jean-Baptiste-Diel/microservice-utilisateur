import re



email = 'jeanbaptiste'
def validation_email(email):
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return jsonify({"message": "Format d'email invalide"}), 400
    # Vérification email unique

validation_email(email)