# News Text Classification

This project now connects the web page text input to the trained ML model through a Flask API.

## Model files required

Place one of the following in the project root:

- `model.joblib` (a full sklearn pipeline), or
- `classifier.joblib` and `vectorizer.joblib`

## Run

```bash
pip install -r requirements.txt
python /home/runner/work/News-Text-Classification/News-Text-Classification/app.py
```

Then open:

- `http://127.0.0.1:5000`

The **Classify** button sends the text to `/predict`, and the model result is displayed in the page.
