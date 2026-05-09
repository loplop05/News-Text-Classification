from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    text = request.json['text']
    prediction = model.predict([text])[0]
    return jsonify({'category': prediction})