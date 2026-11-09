
import math

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_DATA = {
    "age": 35,
    "revenu_mensuel": 250000,
    "montant_credit": 1000000,
    "duree_mois": 12,
    "anciennete_activite": 4,
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_model_info():
    response = client.get("/model-info")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_prediction_valide():
    response = client.post("/predict", json=VALID_DATA)
    assert response.status_code == 200

    result = response.json()
    probability = result["probabilite_defaut"]

    assert math.isfinite(probability)
    assert 0 <= probability <= 1


@pytest.mark.parametrize(
    "field,value",
    [
        ("age", -5),
        ("revenu_mensuel", "inconnu"),
        ("montant_credit", 0),
        ("montant_credit", -1000),
        ("duree_mois", 12.5),
    ],
)
def test_entrees_invalides(field, value):
    data = VALID_DATA.copy()
    data[field] = value

    response = client.post("/predict", json=data)
    assert response.status_code == 422


@pytest.mark.parametrize("field", list(VALID_DATA))
def test_champ_obligatoire_absent(field):
    data = VALID_DATA.copy()
    del data[field]

    response = client.post("/predict", json=data)
    assert response.status_code == 422


def test_champ_supplementaire():
    data = VALID_DATA.copy()
    data["champ_inconnu"] = 123

    response = client.post("/predict", json=data)
    assert response.status_code == 422


def test_json_mal_forme():
    response = client.post(
        "/predict",
        content='{"age": 35,',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


def test_valeur_infinie():
    data = VALID_DATA.copy()
    data["revenu_mensuel"] = "Infinity"

    response = client.post("/predict", json=data)
    assert response.status_code == 422


def test_valeur_extreme():
    data = VALID_DATA.copy()
    data["montant_credit"] = 10**15

    response = client.post("/predict", json=data)

    assert response.status_code in (200, 422)

    if response.status_code == 200:
        probability = response.json()["probabilite_defaut"]
        assert math.isfinite(probability)
        assert 0 <= probability <= 1
