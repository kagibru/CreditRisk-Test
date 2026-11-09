
import json
from pathlib import Path

import joblib
import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.prediction import get_model
from app.preprocessing import to_features
from app.validation import CreditApplication

BASE_DIR = Path(__file__).resolve().parents[1]
BASELINE_PATH = BASE_DIR / "reports" / "baseline.json"

client = TestClient(app)

VALID_DATA = {
    "age": 35,
    "revenu_mensuel": 250000,
    "montant_credit": 1000000,
    "duree_mois": 12,
    "anciennete_activite": 4,
}


def load_baseline():
    with BASELINE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def test_baseline_existe():
    assert BASELINE_PATH.is_file()


def test_baseline_valide():
    baseline = load_baseline()

    assert 0 <= baseline["recall"] <= 1
    assert 0 <= baseline["f1"] <= 1
    assert baseline["n_validation"] == 1000
    assert baseline["seed"] == 42
    assert baseline["synthetic"] is True


def test_contrat_prediction():
    response = client.post("/predict", json=VALID_DATA)

    assert response.status_code == 200

    result = response.json()

    assert "probabilite_defaut" in result
    assert "version_modele" in result
    assert np.isfinite(result["probabilite_defaut"])


def test_prediction_reproductible():
    response1 = client.post("/predict", json=VALID_DATA)
    response2 = client.post("/predict", json=VALID_DATA)

    assert response1.status_code == 200
    assert response2.status_code == 200

    p1 = response1.json()["probabilite_defaut"]
    p2 = response2.json()["probabilite_defaut"]

    assert p1 == pytest.approx(p2, abs=1e-12)


def test_rechargement_modele(tmp_path):
    model = get_model()

    model_path = tmp_path / "model_reload.joblib"
    joblib.dump(model, model_path)

    restored_model = joblib.load(model_path)

    application = CreditApplication(**VALID_DATA)
    features = to_features(application)

    p_original = model.predict_proba(features)[:, 1]
    p_restored = restored_model.predict_proba(features)[:, 1]

    assert np.allclose(
        p_original,
        p_restored,
        atol=1e-10,
        rtol=0,
    )


def test_detection_regression_recall():
    baseline = load_baseline()

    tolerance = 0.02

    # Simulation volontaire d'une nouvelle version degradee.
    nouveau_recall = baseline["recall"] - 0.05

    regression_detectee = (
        nouveau_recall < baseline["recall"] - tolerance
    )

    assert regression_detectee


def test_detection_regression_f1():
    baseline = load_baseline()

    tolerance = 0.02

    # Simulation volontaire d'une nouvelle version degradee.
    nouveau_f1 = baseline["f1"] - 0.05

    regression_detectee = (
        nouveau_f1 < baseline["f1"] - tolerance
    )

    assert regression_detectee
