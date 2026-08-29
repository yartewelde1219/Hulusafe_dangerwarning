from pathlib import Path

import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from ai.feature_extraction.tfidf import build_tfidf_vectorizer
from ai.preprocessing.amharic import preprocess

DANGER_CLASSES = [
    "normal",
    "conflict",
    "flood",
    "fire",
    "landslide",
    "drought",
    "earthquake",
    "extreme_weather",
    "other",
]


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("tfidf", build_tfidf_vectorizer()),
            ("nb", MultinomialNB(alpha=0.1)),
        ]
    )



def predict_proba(pipeline: Pipeline, text: str) -> dict[str, float]:
    processed = preprocess(text)
    probabilities = pipeline.predict_proba([processed])[0]
    return {label: float(prob) for label, prob in zip(pipeline.classes_, probabilities)}


def save_model(pipeline: Pipeline, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, path)


def load_model(path: str | Path) -> Pipeline:
    return joblib.load(path)
