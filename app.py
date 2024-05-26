from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

def preprocess_and_tokenize(data):
    data = re.sub("(<.*?>)", "", data)
    data = re.sub(r'http\S+', '', data)
    data = re.sub(r"(#[\d\w\.]+)", '', data)
    data = re.sub(r"(@[\d\w\.]+)", '', data)
    data = re.sub("(\\W|\\d)", " ", data)
    data = data.strip()
    data = word_tokenize(data)
    porter = PorterStemmer()
    stem_data = [porter.stem(word) for word in data]
    return stem_data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
model = joblib.load('model/model.sav')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        texts = data['texts']
        predictions = model.predict(texts)
        return jsonify(predictions=predictions.tolist())
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
