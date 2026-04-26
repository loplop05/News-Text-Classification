from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pyarabic.araby as araby
from flask import Flask, jsonify, request


BASE_DIR = Path(__file__).resolve().parent

ARABIC_STOPWORDS = {
    "في",
    "من",
    "على",
    "إلى",
    "عن",
    "ما",
    "هو",
    "هي",
    "هذا",
    "هذه",
    "ذلك",
    "تلك",
    "كان",
    "كانت",
    "أو",
    "و",
    "ثم",
    "مع",
    "بين",
    "بعد",
    "قبل",
}


def normalize_arabic(text: str) -> str:
    text = araby.strip_tashkeel(text)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ى", "ي").replace("ة", "ه")
    return text


def remove_noise(text: str) -> str:
    import re

    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[^\u0600-\u06FF\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def light_stem(word: str) -> str:
    prefixes = [
        "مست",
        "است",
        "ال",
        "وال",
        "بال",
        "فال",
        "كال",
        "لل",
        "ب",
        "و",
        "ف",
        "ل",
        "س",
        "ي",
        "ت",
        "ن",
        "أ",
    ]
    suffixes = ["ات", "ون", "ين", "ان", "تم", "كم", "هم", "ها", "ني", "تي", "كن", "هن", "ية", "وا"]

    for prefix in sorted(prefixes, key=len, reverse=True):
        if word.startswith(prefix) and len(word) - len(prefix) >= 3:
            word = word[len(prefix) :]
            break

    for suffix in sorted(suffixes, key=len, reverse=True):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            word = word[: -len(suffix)]
            break

    return word


def preprocess_arabic(text: str) -> str:
    text = normalize_arabic(text)
    text = remove_noise(text)
    tokens = [token for token in text.split() if token not in ARABIC_STOPWORDS and len(token) >= 2]
    tokens = [light_stem(token) for token in tokens]
    return " ".join(tokens)


def _load_model() -> Any:
    pipeline_path = BASE_DIR / "model.joblib"
    if pipeline_path.exists():
        return joblib.load(pipeline_path)

    classifier_path = BASE_DIR / "classifier.joblib"
    vectorizer_path = BASE_DIR / "vectorizer.joblib"
    if classifier_path.exists() and vectorizer_path.exists():
        classifier = joblib.load(classifier_path)
        vectorizer = joblib.load(vectorizer_path)
        return {"classifier": classifier, "vectorizer": vectorizer}

    raise FileNotFoundError(
        "No model artifact found. Add model.joblib, or classifier.joblib + vectorizer.joblib to the project root."
    )


MODEL = _load_model()
app = Flask(__name__, static_folder=".", static_url_path="")


@app.get("/")
def home():
    return app.send_static_file("index.html")


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Text is required."}), 400

    processed = preprocess_arabic(text)
    if not processed:
        return jsonify({"error": "Text does not contain valid Arabic words after preprocessing."}), 400

    classes = None
    if isinstance(MODEL, dict):
        features = MODEL["vectorizer"].transform([processed])
        prediction = MODEL["classifier"].predict(features)[0]
        probabilities = (
            MODEL["classifier"].predict_proba(features)[0] if hasattr(MODEL["classifier"], "predict_proba") else None
        )
        classes = getattr(MODEL["classifier"], "classes_", None)
    else:
        prediction = MODEL.predict([processed])[0]
        probabilities = MODEL.predict_proba([processed])[0] if hasattr(MODEL, "predict_proba") else None
        classes = getattr(MODEL, "classes_", None)

    response = {"category": str(prediction)}
    if probabilities is not None and classes is not None:
        confidence = max(float(prob) for prob in probabilities)
        response["confidence"] = confidence

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
