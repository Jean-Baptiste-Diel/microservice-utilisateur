
from nltk import word_tokenize
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from utils import fonction

# Charger le modèle
model = load_model('C:/Users/Jean Baptiste/Desktop/Memoire/Model/best_model.keras', compile=False, safe_mode=False)

# Charger le tokenizer sauvegardé
with open('C:/Users/Jean Baptiste/Desktop/Memoire/Model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Nettoyage du texte
def nettoyer_texte(texte):
    texte = texte.lower()  # Normalisation
    texte = re.sub(r'[^>]*', '', texte)  # Supprimer les balises HTML
    texte = re.sub(r'[^a-zA-Z\s]', '', texte)  # Supprimer les caractères spéciaux
    texte.split()
    mots = word_tokenize(texte)  # Tokenisation ici
    stop_words = set(stopwords.words('french'))
    mots = [mot for mot in mots if mot not in stop_words]
    lemmatizer = WordNetLemmatizer()
    mots = [lemmatizer.lemmatize(mot) for mot in mots]
    return ' '.join(mots)

MAX_LENGTH = 200
def predict_sentiment(text):
    # Prétraitement
    cleaned_text = fonction.nettoyer_texte(text)
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded = pad_sequences(sequence, maxlen=MAX_LENGTH)
    # Prédiction
    prediction = model.predict(padded)[0][0]
    confidence = round(max(prediction, 1 - prediction) * 100, 2)
    label = 'POSITIF' if prediction > 0.5 else 'NÉGATIF'

    print(f"\nTexte : {text}")
    print(f"Prédiction : {label} ({confidence}% de confiance)")
    print(f"Score brut : {round(prediction, 4)}")

    return prediction