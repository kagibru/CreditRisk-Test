
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


# Tests complémentaires pour la validation des champs numériques

@pytest.mark.parametrize(
    "age",
    [17, 101, -1, 18.5, "35", True],
)
def test_age_invalide(age):
    data = VALID_DATA.copy()
    data["age"] = age

    response = client.post("/predict", json=data)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "field,value",
    [
        ("revenu_mensuel", 0),
        ("revenu_mensuel", -1000),
        ("revenu_mensuel", 100_000_001),
        ("montant_credit", 1_000_000_001),
        ("duree_mois", 0),
        ("duree_mois", 361),
        ("anciennete_activite", -1),
        ("anciennete_activite", 81),
    ],
)
def test_valeurs_hors_limites_complementaires(field, value):
    data = VALID_DATA.copy()
    data[field] = value

    response = client.post("/predict", json=data)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "field,value",
    [
        ("age", 18),
        ("age", 100),
        ("revenu_mensuel", 0.01),
        ("revenu_mensuel", 100_000_000),
        ("montant_credit", 0.01),
        ("montant_credit", 1_000_000_000),
        ("duree_mois", 1),
        ("duree_mois", 360),
        ("anciennete_activite", 0),
        ("anciennete_activite", 80),
    ],
)
def test_valeurs_limites_valides(field, value):
    data = VALID_DATA.copy()
    data[field] = value

    response = client.post("/predict", json=data)

    assert response.status_code == 200

    probability = response.json()["probabilite_defaut"]
    assert math.isfinite(probability)
    assert 0 <= probability <= 1
