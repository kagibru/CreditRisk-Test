
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import f1_score, recall_score
from sklearn.model_selection import train_test_split

from app.prediction import get_model

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "reports" / "baseline.json"

TOLERANCE = 0.02


def generate_validation_data(seed=42):
    rng = np.random.default_rng(seed)
    n = 4000

    age = rng.integers(18, 76, n)
    income = rng.uniform(50_000, 1_500_000, n)
    amount = rng.uniform(50_000, 15_000_000, n)
    duration = rng.integers(3, 61, n)
    seniority = rng.uniform(0, 30, n)

    X = np.column_stack(
        (age, income, amount, duration, seniority)
    )

    score = (
        -2.0
        + 0.9 * (amount / (income * duration))
        - 0.05 * seniority
    )

    p = 1 / (1 + np.exp(-np.clip(score, -20, 20)))
    y = rng.binomial(1, p)

    _, X_val, _, y_val = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    return X_val, y_val


def test_model_metrics_against_baseline():
    with BASELINE_PATH.open(encoding="utf-8") as f:
        baseline = json.load(f)

    X_val, y_val = generate_validation_data(
        seed=baseline["seed"]
    )

    assert len(y_val) == baseline["n_validation"]

    model = get_model()
    predictions = model.predict(X_val)

    current_recall = recall_score(
        y_val, predictions, zero_division=0
    )

    current_f1 = f1_score(
        y_val, predictions, zero_division=0
    )

    print(f"\nRecall actuel : {current_recall:.4f}")
    print(f"Recall baseline : {baseline['recall']:.4f}")
    print(f"F1 actuel : {current_f1:.4f}")
    print(f"F1 baseline : {baseline['f1']:.4f}")

    assert current_recall >= baseline["recall"] - TOLERANCE, (
        "Regression detectee sur le recall"
    )

    assert current_f1 >= baseline["f1"] - TOLERANCE, (
        "Regression detectee sur le F1-score"
    )
