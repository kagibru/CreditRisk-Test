
import statistics
import time

import numpy as np
from fastapi.testclient import TestClient

from app.main import app
from app.prediction import predict_probability
from app.preprocessing import to_features
from app.validation import CreditApplication

client = TestClient(app)

DATA = {
    "age": 35,
    "revenu_mensuel": 250000,
    "montant_credit": 1000000,
    "duree_mois": 12,
    "anciennete_activite": 4,
}


def test_performance_api():
    # Prechauffage
    for _ in range(10):
        assert client.post("/predict", json=DATA).status_code == 200

    latencies = []

    for _ in range(100):
        start = time.perf_counter()
        response = client.post("/predict", json=DATA)
        elapsed = time.perf_counter() - start

        assert response.status_code == 200
        latencies.append(elapsed)

    p95 = float(np.percentile(latencies, 95))
    average = statistics.mean(latencies)
    throughput = len(latencies) / sum(latencies)

    print(f"\nLatence API moyenne : {average * 1000:.2f} ms")
    print(f"Latence API P95 : {p95 * 1000:.2f} ms")
    print(f"Debit sequentiel : {throughput:.2f} req/s")

    assert np.isfinite(p95)
    assert p95 > 0


def test_performance_inference():
    application = CreditApplication(**DATA)
    features = to_features(application)

    # Prechauffage
    for _ in range(10):
        predict_probability(features)

    latencies = []

    for _ in range(100):
        start = time.perf_counter()
        probability = predict_probability(features)
        elapsed = time.perf_counter() - start

        assert 0 <= probability <= 1
        latencies.append(elapsed)

    p95 = float(np.percentile(latencies, 95))

    print(f"\nLatence inference P95 : {p95 * 1000:.2f} ms")

    assert np.isfinite(p95)
    assert p95 > 0
