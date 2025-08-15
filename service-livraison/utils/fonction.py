import re

from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords

def nettoyer_texte(texte):
    texte = texte.lower()  # Normalisation
    texte = re.sub(r'<.*?>', '', texte)  # Supprimer les balises HTML
    texte = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', texte)  # Conserver les caractères alphabétiques avec accents
    mots = word_tokenize(texte, language='french')  # Tokenisation en français
    stop_words = set(stopwords.words('french'))
    mots = [mot for mot in mots if mot not in stop_words]  # Suppression des stopwords
    stemmer = SnowballStemmer('french')  # Utilisation du stemmer français
    mots = [stemmer.stem(mot) for mot in mots]  # Stemming
    return ' '.join(mots)