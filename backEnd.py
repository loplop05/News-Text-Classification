from flask import Flask, request, jsonify, render_template
import pickle
import re
import pyarabic.araby as araby

app = Flask(__name__)

try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    print("Warning: model.pkl not found. Please run train_model.py first.")

def remove_diacritics(text):
    return araby.strip_tashkeel(text)

def normalize_arabic(text):
    text = re.sub('[إأآا]', 'ا', text)
    text = re.sub('ة', 'ه', text)
    text = re.sub('ى', 'ي', text)
    return text

def remove_noise(text):
    text = re.sub(r'http\S+|www.\S+', '', text)
    text = re.sub(r'[^\u0600-\u06FF\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_arabic(text):
    text = remove_diacritics(text)
    text = normalize_arabic(text)
    text = remove_noise(text)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    processed_text = preprocess_arabic(text)
    
    prediction = model.predict([processed_text])[0]
    
    label_map = {
        'رياضة': 'رياضة (Sports)',
        'سياسة': 'سياسة (Politics)',
        'اقتصاد': 'اقتصاد (Economy)'
    }
    
    category = label_map.get(prediction, prediction)
    
    return jsonify({'category': category})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
