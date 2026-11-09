
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


@pytest.mark.parametrize(
    "field,value",
    [
        ("age", None),
        ("revenu_mensuel", None),
        ("montant_credit", None),
        ("duree_mois", None),
        ("anciennete_activite", None),
        ("revenu_mensuel", "abc"),
        ("montant_credit", "invalide"),
        ("age", -1),
        ("montant_credit", -500),
        ("duree_mois", 0),
    ],
)
def test_entrees_invalides(field, value):
    data = VALID_DATA.copy()
    data[field] = value

    response = client.post("/predict", json=data)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field,value",
    [
        ("age", 0),
        ("age", 150),
        ("duree_mois", 1200),
        ("anciennete_activite", -5),
    ],
)
def test_valeurs_hors_limites(field, value):
    data = VALID_DATA.copy()
    data[field] = value

    response = client.post("/predict", json=data)

    assert response.status_code == 422


def test_schema_incorrect():
    response = client.post(
        "/predict",
        json={"champ_inconnu": 123},
    )

    assert response.status_code == 422


def test_probabilite_finie():
    response = client.post("/predict", json=VALID_DATA)

    assert response.status_code == 200

    probability = response.json()["probabilite_defaut"]

    assert math.isfinite(probability)
    assert 0 <= probability <= 1


def test_prediction_repetable():
    response1 = client.post("/predict", json=VALID_DATA)
    response2 = client.post("/predict", json=VALID_DATA)

    assert response1.status_code == 200
    assert response2.status_code == 200

    p1 = response1.json()["probabilite_defaut"]
    p2 = response2.json()["probabilite_defaut"]

    assert p1 == pytest.approx(p2, abs=1e-12)


def test_montant_extreme():
    data = VALID_DATA.copy()
    data["montant_credit"] = 10**15

    response = client.post("/predict", json=data)

    assert response.status_code in (200, 422)

    if response.status_code == 200:
        probability = response.json()["probabilite_defaut"]
        assert math.isfinite(probability)
        assert 0 <= probability <= 1
