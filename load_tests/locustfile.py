
from locust import HttpUser, between, task


class CreditRiskUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict_credit_risk(self):
        payload = {
            "age": 35,
            "revenu_mensuel": 250000,
            "montant_credit": 1000000,
            "duree_mois": 12,
            "anciennete_activite": 4,
        }

        with self.client.post(
            "/predict",
            json=payload,
            name="POST /predict",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"HTTP {response.status_code}"
                )
                return

            try:
                result = response.json()
                probability = result["probabilite_defaut"]

                if not 0 <= probability <= 1:
                    response.failure(
                        "Probabilite hors limites"
                    )
                else:
                    response.success()

            except (ValueError, KeyError, TypeError):
                response.failure(
                    "Reponse JSON invalide"
                )
