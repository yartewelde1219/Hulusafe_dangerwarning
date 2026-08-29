from datetime import datetime, timezone
from pathlib import Path
import json
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai.models.naive_bayes import build_pipeline, save_model
from ai.preprocessing.amharic import preprocess

DATASET = Path(__file__).resolve().parents[1] / "dataset" / "sample_articles.jsonl"
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "naive_bayes.joblib"



def load_dataset(path: Path = DATASET) -> tuple[list[str], list[str]]:
    texts: list[str] = []
    labels: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        texts.append(preprocess(row["text"]))
        labels.append(row["label"])
    return texts, labels


def main() -> None:
    texts, labels = load_dataset()
    pipeline = build_pipeline()
    pipeline.fit(texts, labels)
    save_model(pipeline, MODEL_PATH)
    print(f"Trained on {len(texts)} examples at {datetime.now(timezone.utc).isoformat()}")
    print(f"Saved {MODEL_PATH}")


if __name__ == "__main__":
    main()
