from pathlib import Path
import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "credit_model.joblib"
_model = None


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError("Modele indisponible")
        _model = joblib.load(MODEL_PATH)  # Charger uniquement un artefact de confiance.
    return _model


def predict_probability(features):
    result = float(get_model().predict_proba(features)[0, 1])
    if not np.isfinite(result) or not 0 <= result <= 1:
        raise ValueError("Probabilite invalide")
    return result
