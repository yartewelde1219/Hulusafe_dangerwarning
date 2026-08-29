import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

from ai.models.naive_bayes import load_model, predict_proba
from ai.training.train import load_dataset, MODEL_PATH, DATASET
from ai.information_extraction.negation import analyze_context, is_active_danger_language



def evaluate(y_true: list[str], y_pred: list[str]) -> dict:
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    matrix = confusion_matrix(y_true, y_pred).tolist()
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    return {
        "accuracy": float(acc),
        "macro_f1": float(macro_f1),
        "classification_report": report,
        "confusion_matrix": matrix,
    }


def evaluate_false_alarm_scenarios() -> dict:
    """Evaluate critical false-alarm cases (negation, historical, hypothetical)."""
    dataset_path = DATASET
    test_cases = []
    for line in dataset_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        test_cases.append(json.loads(line))

    negation_passed = 0
    negation_total = 0
    historical_passed = 0
    historical_total = 0
    hypothetical_passed = 0
    hypothetical_total = 0

    for case in test_cases:
        text = case["text"]
        context = analyze_context(text)
        is_active = is_active_danger_language(text)

        if case.get("negated"):
            negation_total += 1
            if context["negated"] and not is_active:
                negation_passed += 1

        if case.get("historical"):
            historical_total += 1
            if context["historical"] and not is_active:
                historical_passed += 1

        if case.get("hypothetical"):
            hypothetical_total += 1
            if context["hypothetical"] and not is_active:
                hypothetical_passed += 1

    return {
        "negation_detection": {
            "passed": negation_passed,
            "total": negation_total,
            "rate": negation_passed / max(negation_total, 1),
        },
        "historical_detection": {
            "passed": historical_passed,
            "total": historical_total,
            "rate": historical_passed / max(historical_total, 1),
        },
        "hypothetical_detection": {
            "passed": hypothetical_passed,
            "total": hypothetical_total,
            "rate": hypothetical_passed / max(hypothetical_total, 1),
        },
    }


def run_evaluation_report() -> None:
    texts, labels = load_dataset()
    if not MODEL_PATH.exists():
        print(f"Model not found at {MODEL_PATH}. Training first...")
        from ai.training.train import main as train_main
        train_main()

    model = load_model(MODEL_PATH)
    predictions = model.predict(texts)

    eval_results = evaluate(labels, predictions)
    print("=" * 60)
    print("HuluSafe Amharic Danger Classification Evaluation")
    print("=" * 60)
    print(f"Total evaluated samples: {len(texts)}")
    print(f"Accuracy: {eval_results['accuracy']:.4f}")
    print(f"Macro F1-Score: {eval_results['macro_f1']:.4f}")
    print("-" * 60)
    print("Per-class performance:")
    for cls, metrics in eval_results["classification_report"].items():
        if isinstance(metrics, dict):
            print(f"  {cls:<16} Precision: {metrics['precision']:.2f} | Recall: {metrics['recall']:.2f} | F1: {metrics['f1-score']:.2f} (Support: {metrics['support']})")

    print("=" * 60)
    print("Critical False-Alarm Evaluation (Negation / Historical / Hypothetical)")
    print("=" * 60)
    edge_results = evaluate_false_alarm_scenarios()
    for name, res in edge_results.items():
        print(f"  {name:<24}: {res['passed']}/{res['total']} passed ({res['rate'] * 100:.1f}%)")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation_report()

