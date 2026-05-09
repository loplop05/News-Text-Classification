import pandas as pd
import re
import pickle
import pyarabic.araby as araby
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

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

# Load data
df = pd.read_csv('arabic_news.csv', encoding='utf-8-sig')

df['clean_text'] = df['text'].apply(preprocess_arabic)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
    ('clf', LogisticRegression())
])

# Train
pipeline.fit(df['clean_text'], df['label'])

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(pipeline, f)


