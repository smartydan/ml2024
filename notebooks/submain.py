from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
import string
import pickle
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

stop_words = set(stopwords.words('english'))

RANDOM_STATE = 42

morph = WordNetLemmatizer()

def rm_punc(text):
    text = str(text)
    for el in string.punctuation:
        text = text.replace(el, '')
    return text.lower()

def rm_stopwords(text):
    return ' '.join([word for word in text.split() if word.lower() not in stop_words])

def get(word):
    return morph.lemmatize(word)

def func(text):
    return " ".join([get(word) for word in text.split()])

def save(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)