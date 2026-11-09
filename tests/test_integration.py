
import math

import joblib
import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.preprocessing import to_features
from app.validation import CreditApplication
from app.prediction import get_model, predict_probability

client = TestClient(app)

VALID_DATA = {
    "age": 35,
    "revenu_mensuel": 250000,
    "montant_credit": 1000000,
    "duree_mois": 12,
    "anciennete_activite": 4,
}


def test_pipeline_complet():
    """Validation -> preprocessing -> modele -> API."""
    response = client.post("/predict", json=VALID_DATA)

    assert response.status_code == 200

    result = response.json()

    assert "probabilite_defaut" in result
    assert "version_modele" in result
    assert math.isfinite(result["probabilite_defaut"])
    assert 0 <= result["probabilite_defaut"] <= 1


def test_dimensions_preprocessing():
    application = CreditApplication(**VALID_DATA)
    features = to_features(application)

    assert isinstance(features, np.ndarray)
    assert features.shape == (1, 5)
    assert np.isfinite(features).all()


def test_prediction_directe_et_api():
    application = CreditApplication(**VALID_DATA)
    features = to_features(application)

    direct = predict_probability(features)

    response = client.post("/predict", json=VALID_DATA)

    assert response.status_code == 200

    api_probability = response.json()["probabilite_defaut"]

    assert np.isclose(direct, api_probability, atol=1e-10)


def test_modele_disponible():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metadonnees_modele():
    response = client.get("/model-info")

    assert response.status_code == 200

    result = response.json()

    assert result["version"] == "1.0.0"
    assert result["type"] == "LogisticRegression"
    assert result["production_ready"] is False


def test_modele_indisponible(monkeypatch):
    def unavailable():
        raise FileNotFoundError("Modele absent")

    monkeypatch.setattr("app.main.get_model", unavailable)

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["detail"] == "Modele indisponible"


def test_modele_indisponible_prediction(monkeypatch):
    def unavailable(_features):
        raise FileNotFoundError("Modele absent")

    monkeypatch.setattr(
        "app.main.predict_probability",
        unavailable,
    )

    response = client.post("/predict", json=VALID_DATA)

    assert response.status_code == 503
    assert response.json()["detail"] == "Modele indisponible"


def test_erreur_preprocessing(monkeypatch):
    def invalid_features(_application):
        raise ValueError("Erreur de transformation")

    monkeypatch.setattr("app.main.to_features", invalid_features)

    response = client.post("/predict", json=VALID_DATA)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erreur de prediction"
    assert "Erreur de transformation" not in response.text


def test_dimensions_incorrectes():
    model = get_model()

    invalid_features = np.zeros((1, 4))

    with pytest.raises(ValueError):
        model.predict_proba(invalid_features)


def test_erreur_prediction_interne(monkeypatch):
    def internal_error(_features):
        raise ValueError("Erreur interne sensible")

    monkeypatch.setattr(
        "app.main.predict_probability",
        internal_error,
    )

    response = client.post("/predict", json=VALID_DATA)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erreur de prediction"
    assert "Erreur interne sensible" not in response.text


def test_sauvegarde_rechargement(tmp_path):
    model = get_model()

    path = tmp_path / "model_test.joblib"
    joblib.dump(model, path)

    reloaded = joblib.load(path)

    application = CreditApplication(**VALID_DATA)
    features = to_features(application)

    original = model.predict_proba(features)[:, 1]
    restored = reloaded.predict_proba(features)[:, 1]

    assert np.allclose(original, restored, atol=1e-10)
