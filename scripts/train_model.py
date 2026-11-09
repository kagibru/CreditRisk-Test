"""Donnees entierement synthetiques : demonstration QA uniquement."""
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]


def main():
    rng = np.random.default_rng(42)
    n = 4000
    age = rng.integers(18, 76, n)
    income = rng.uniform(50_000, 1_500_000, n)
    amount = rng.uniform(50_000, 15_000_000, n)
    duration = rng.integers(3, 61, n)
    seniority = rng.uniform(0, 30, n)
    X = np.column_stack((age, income, amount, duration, seniority))
    # Regle artificielle, non validee pour une utilisation bancaire.
    score = -2.0 + 0.9 * (amount / (income * duration)) - 0.05 * seniority
    p = 1 / (1 + np.exp(-np.clip(score, -20, 20)))
    y = rng.binomial(1, p)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = Pipeline([("scaler", StandardScaler()), ("classifier", LogisticRegression(max_iter=1000, random_state=42))])
    model.fit(X_train, y_train)
    predictions = model.predict(X_val)
    metrics = {"recall": float(recall_score(y_val, predictions, zero_division=0)), "f1": float(f1_score(y_val, predictions, zero_division=0)), "n_validation": len(y_val), "seed": 42, "synthetic": True}
    (ROOT / "models").mkdir(exist_ok=True)
    (ROOT / "reports").mkdir(exist_ok=True)
    joblib.dump(model, ROOT / "models" / "credit_model.joblib")
    (ROOT / "reports" / "baseline.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("Modele enregistre ; metriques :", metrics)


if __name__ == "__main__":
    main()
