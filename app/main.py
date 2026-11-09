from fastapi import FastAPI, HTTPException
from app.validation import CreditApplication
from app.preprocessing import to_features
from app.prediction import get_model, predict_probability

app = FastAPI(title="CreditRisk-Test", version="1.0.0")


@app.get("/health")
def health():
    try:
        get_model()
    except (FileNotFoundError, OSError, ValueError):
        raise HTTPException(status_code=503, detail="Modele indisponible") from None
    return {"status": "ok"}


@app.get("/model-info")
def model_info():
    try:
        get_model()
    except (FileNotFoundError, OSError, ValueError):
        raise HTTPException(status_code=503, detail="Modele indisponible") from None
    return {"version": "1.0.0", "type": "LogisticRegression", "data": "synthetic", "production_ready": False}


@app.post("/predict")
def predict(payload: CreditApplication):
    try:
        probability = predict_probability(to_features(payload))
    except (FileNotFoundError, OSError):
        raise HTTPException(status_code=503, detail="Modele indisponible") from None
    except (ValueError, IndexError):
        raise HTTPException(status_code=500, detail="Erreur de prediction") from None
    return {"probabilite_defaut": probability, "version_modele": "1.0.0"}
