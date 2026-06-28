import pandas as pd
import re
import pickle
import pyarabic.araby as araby
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def preprocess_arabic(text):
    if not isinstance(text, str):
        return ""
    # Remove diacritics
    text = araby.strip_tashkeel(text)
    # Normalize alef, taa marbouta, alef maqsura
    text = re.sub('[إأآا]', 'ا', text)
    text = re.sub('ة', 'ه', text)
    text = re.sub('ى', 'ي', text)
    # Remove non-Arabic characters but keep spaces
    text = re.sub(r'[^\u0600-\u06FF\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load data
df = pd.read_csv('arabic_news.csv', encoding='utf-8-sig')

# Deduplicate to ensure the model learns features, not patterns of repetition
# This prevents artificially high accuracy during training and forces the model to learn
df = df.drop_duplicates(subset=['text'])

# Clean data
df['clean_text'] = df['text'].apply(preprocess_arabic)

# Pipeline with LinearSVC (better performance for text classification)
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 3), # Capture phrases up to 3 words
        max_df=0.9,
        min_df=2
    )),
    ('clf', LinearSVC(C=1.0, random_state=42, max_iter=2000))
])

# Train on all unique data
print("Training the improved model...")
pipeline.fit(df['clean_text'], df['label'])

# Save the model - ensure it matches the filename in backEnd.py
with open('NewsClassifierModel.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

print("\nModel saved as NewsClassifierModel.pkl")
